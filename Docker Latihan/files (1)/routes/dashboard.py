from flask import Blueprint, render_template, request, redirect, url_for, flash, session, \
    jsonify, send_file, Response, current_app
from functools import wraps
import io, mimetypes, humanize
from services import auth_service, file_service, minio_service

bp = Blueprint('dashboard', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    return auth_service.get_user_by_id(session['user_id'])

def fmt_size(n):
    if n is None: return '0 B'
    return humanize.naturalsize(n, binary=True)

@bp.context_processor
def inject_user():
    if session.get('user_id'):
        user = get_current_user()
        if user:
            quota = user['storage_quota'] or 1
            pct = min(100, round((user['storage_used'] or 0) / quota * 100, 1))
            return dict(current_user=user, storage_pct=pct,
                        fmt_size=fmt_size,
                        file_icon=file_service.get_file_icon,
                        file_color=file_service.get_file_color)
    return dict(current_user=None, storage_pct=0, fmt_size=fmt_size,
                file_icon=file_service.get_file_icon,
                file_color=file_service.get_file_color)

# ─── Main Dashboard ───────────────────────────────────────────────────────────
@bp.route('/')
@login_required
def index():
    uid = session['user_id']
    folder_id = request.args.get('folder', type=int)
    search = request.args.get('q', '').strip()
    ftype = request.args.get('type', '').strip()
    view = request.args.get('view', 'grid')
    
    folders = file_service.get_folders(uid, folder_id)
    files = file_service.get_files(uid, folder_id, search or None, ftype or None)
    breadcrumb = file_service.get_breadcrumb(folder_id, uid) if folder_id else []
    current_folder = file_service.get_folder_by_id(folder_id, uid) if folder_id else None
    recent = file_service.get_recent_files(uid, 5) if not folder_id and not search else []
    storage_by_type = file_service.get_storage_by_type(uid)
    
    return render_template('dashboard/index.html',
        folders=folders, files=files, breadcrumb=breadcrumb,
        current_folder=current_folder, recent=recent,
        storage_by_type=storage_by_type,
        search=search, ftype=ftype, view=view,
        folder_id=folder_id,
    )

@bp.route('/starred')
@login_required
def starred():
    uid = session['user_id']
    files = file_service.get_starred_files(uid)
    return render_template('dashboard/starred.html', files=files)

@bp.route('/recent')
@login_required  
def recent():
    uid = session['user_id']
    files = file_service.get_recent_files(uid, 50)
    return render_template('dashboard/recent.html', files=files)

# ─── Folder Operations ────────────────────────────────────────────────────────
@bp.route('/folder/create', methods=['POST'])
@login_required
def create_folder():
    uid = session['user_id']
    name = request.form.get('name', '').strip()
    parent_id = request.form.get('parent_id', type=int)
    color = request.form.get('color', '#6366f1')
    
    if not name:
        flash('Nama folder tidak boleh kosong.', 'error')
    else:
        file_service.create_folder(uid, name, parent_id, color)
        auth_service.log_activity(uid, 'create_folder', 'folder', None, name)
        flash(f'Folder "{name}" berhasil dibuat.', 'success')
    
    return redirect(url_for('dashboard.index', folder=parent_id))

@bp.route('/folder/<int:folder_id>/rename', methods=['POST'])
@login_required
def rename_folder(folder_id):
    uid = session['user_id']
    new_name = request.form.get('name', '').strip()
    if new_name:
        file_service.rename_folder(folder_id, uid, new_name)
        return jsonify({'success': True, 'name': new_name})
    return jsonify({'success': False}), 400

@bp.route('/folder/<int:folder_id>/delete', methods=['POST'])
@login_required
def delete_folder(folder_id):
    uid = session['user_id']
    folder = file_service.get_folder_by_id(folder_id, uid)
    if folder:
        total_size = file_service.delete_folder_recursive(folder_id, uid)
        auth_service.update_user_storage(uid, -total_size)
        auth_service.log_activity(uid, 'delete_folder', 'folder', folder_id, folder['name'])
        flash(f'Folder "{folder["name"]}" dan semua isinya berhasil dihapus.', 'success')
    return redirect(url_for('dashboard.index'))

# ─── File Operations ──────────────────────────────────────────────────────────
@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    uid = session['user_id']
    user = get_current_user()
    folder_id = request.form.get('folder_id', type=int)
    files = request.files.getlist('files')
    
    if not files or all(f.filename == '' for f in files):
        return jsonify({'success': False, 'message': 'Tidak ada file dipilih.'}), 400
    
    uploaded = []
    errors = []
    
    for file in files:
        if not file.filename:
            continue
        
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        
        available = (user['storage_quota'] or 0) - (user['storage_used'] or 0)
        if size > available:
            errors.append(f"{file.filename}: Storage penuh.")
            continue
        
        mime = file.content_type or mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
        ftype = file_service.detect_file_type(file.filename)
        object_key = minio_service.generate_object_key(uid, file.filename)
        
        try:
            minio_service.upload_file(file, object_key, mime, size)
            file_id = file_service.create_file_record(
                uid, folder_id, file.filename, file.filename,
                object_key, size, mime, ftype
            )
            auth_service.update_user_storage(uid, size)
            auth_service.log_activity(uid, 'upload', 'file', file_id, file.filename)
            uploaded.append({'id': file_id, 'name': file.filename, 'size': fmt_size(size)})
        except Exception as e:
            errors.append(f"{file.filename}: Upload gagal - {str(e)}")
    
    return jsonify({
        'success': len(uploaded) > 0,
        'uploaded': uploaded,
        'errors': errors,
        'message': f'{len(uploaded)} file berhasil diupload.' + (f' {len(errors)} gagal.' if errors else '')
    })

@bp.route('/file/<int:file_id>/download')
@login_required
def download(file_id):
    uid = session['user_id']
    f = file_service.get_file_by_id(file_id, uid)
    if not f:
        flash('File tidak ditemukan.', 'error')
        return redirect(url_for('dashboard.index'))
    
    try:
        stream = minio_service.get_file_stream(f['object_key'])
        file_service.increment_download(file_id)
        auth_service.log_activity(uid, 'download', 'file', file_id, f['name'])
        
        return Response(
            stream,
            headers={
                'Content-Disposition': f'attachment; filename="{f["original_name"]}"',
                'Content-Type': f['mime_type'],
                'Content-Length': str(f['size']),
            }
        )
    except Exception as e:
        flash(f'Gagal mengunduh file: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@bp.route('/file/<int:file_id>/preview')
@login_required
def preview(file_id):
    uid = session['user_id']
    f = file_service.get_file_by_id(file_id, uid)
    if not f:
        return jsonify({'error': 'File not found'}), 404
    url = minio_service.get_presigned_url(f['object_key'], expires_hours=1)
    return jsonify({'url': url, 'name': f['name'], 'type': f['file_type'], 'mime': f['mime_type']})

@bp.route('/file/<int:file_id>/rename', methods=['POST'])
@login_required
def rename_file(file_id):
    uid = session['user_id']
    new_name = request.form.get('name', '').strip()
    if new_name:
        file_service.rename_file(file_id, uid, new_name)
        auth_service.log_activity(uid, 'rename', 'file', file_id, new_name)
        return jsonify({'success': True, 'name': new_name})
    return jsonify({'success': False}), 400

@bp.route('/file/<int:file_id>/move', methods=['POST'])
@login_required
def move_file(file_id):
    uid = session['user_id']
    folder_id = request.form.get('folder_id', type=int)
    file_service.move_file(file_id, uid, folder_id)
    return jsonify({'success': True})

@bp.route('/file/<int:file_id>/star', methods=['POST'])
@login_required
def toggle_star(file_id):
    uid = session['user_id']
    is_starred = file_service.toggle_star(file_id, uid)
    return jsonify({'success': True, 'starred': bool(is_starred)})

@bp.route('/file/<int:file_id>/share', methods=['POST'])
@login_required
def share_file(file_id):
    uid = session['user_id']
    action = request.form.get('action', 'share')
    if action == 'unshare':
        file_service.unshare_file(file_id, uid)
        return jsonify({'success': True, 'shared': False})
    token = file_service.generate_share_token(file_id, uid)
    share_url = url_for('dashboard.shared_file', token=token, _external=True)
    return jsonify({'success': True, 'shared': True, 'url': share_url, 'token': token})

@bp.route('/file/<int:file_id>/delete', methods=['POST'])
@login_required
def delete_file(file_id):
    uid = session['user_id']
    f = file_service.get_file_by_id(file_id, uid)
    if f:
        size = file_service.delete_file_record(file_id, uid)
        if size:
            auth_service.update_user_storage(uid, -size)
        auth_service.log_activity(uid, 'delete', 'file', file_id, f['name'])
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'File not found'}), 404

# ─── Shared File ──────────────────────────────────────────────────────────────
@bp.route('/share/<token>')
def shared_file(token):
    f = file_service.get_file_by_share_token(token)
    if not f:
        return render_template('dashboard/not_found.html'), 404
    owner = auth_service.get_user_by_id(f['user_id'])
    url = minio_service.get_presigned_url(f['object_key'], expires_hours=24)
    return render_template('dashboard/shared.html', file=f, owner=owner, download_url=url,
                           fmt_size=fmt_size, file_icon=file_service.get_file_icon,
                           file_color=file_service.get_file_color)

@bp.route('/share/<token>/download')
def download_shared(token):
    f = file_service.get_file_by_share_token(token)
    if not f:
        return 'File not found', 404
    try:
        stream = minio_service.get_file_stream(f['object_key'])
        file_service.increment_download(f['id'])
        return Response(
            stream,
            headers={
                'Content-Disposition': f'attachment; filename="{f["original_name"]}"',
                'Content-Type': f['mime_type'],
            }
        )
    except Exception as e:
        return str(e), 500

# ─── Settings ─────────────────────────────────────────────────────────────────
@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    uid = session['user_id']
    user = get_current_user()
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'change_password':
            from werkzeug.security import check_password_hash
            current_pw = request.form.get('current_password')
            new_pw = request.form.get('new_password')
            confirm_pw = request.form.get('confirm_password')
            
            if not check_password_hash(user['password'], current_pw):
                flash('Password lama salah.', 'error')
            elif len(new_pw) < 8:
                flash('Password baru minimal 8 karakter.', 'error')
            elif new_pw != confirm_pw:
                flash('Konfirmasi password tidak cocok.', 'error')
            else:
                auth_service.update_password(uid, new_pw)
                flash('Password berhasil diubah.', 'success')
    
    activity = auth_service.get_user_by_id(uid)
    logs = []
    return render_template('dashboard/settings.html', user=user, activity_logs=logs)
