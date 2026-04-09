import os, mimetypes, secrets
from services.db import query, execute
from services import minio_service
from config import Config

ICON_MAP = {
    'image': 'fa-image', 'video': 'fa-film', 'audio': 'fa-music',
    'document': 'fa-file-alt', 'archive': 'fa-file-archive',
    'code': 'fa-code', 'other': 'fa-file',
}
COLOR_MAP = {
    'image': '#10b981', 'video': '#8b5cf6', 'audio': '#f59e0b',
    'document': '#3b82f6', 'archive': '#ef4444', 'code': '#6366f1', 'other': '#6b7280',
}

def detect_file_type(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    for ftype, exts in Config.ALLOWED_EXTENSIONS.items():
        if ext in exts:
            return ftype
    return 'other'

def get_file_icon(file_type):
    return ICON_MAP.get(file_type, 'fa-file')

def get_file_color(file_type):
    return COLOR_MAP.get(file_type, '#6b7280')

def get_files(user_id, folder_id=None, search=None, file_type=None, starred=False):
    conditions = ["user_id=%s"]
    params = [user_id]
    if folder_id is not None:
        conditions.append("folder_id=%s")
        params.append(folder_id)
    else:
        conditions.append("folder_id IS NULL")
    if search:
        conditions.append("name LIKE %s")
        params.append(f"%{search}%")
    if file_type:
        conditions.append("file_type=%s")
        params.append(file_type)
    if starred:
        conditions.append("is_starred=1")
    where = " AND ".join(conditions)
    return query(f"SELECT * FROM files WHERE {where} ORDER BY created_at DESC", params)

def search_all_files(user_id, search, file_type=None):
    conditions = ["user_id=%s", "name LIKE %s"]
    params = [user_id, f"%{search}%"]
    if file_type:
        conditions.append("file_type=%s")
        params.append(file_type)
    where = " AND ".join(conditions)
    return query(f"SELECT * FROM files WHERE {where} ORDER BY created_at DESC", params)

def get_starred_files(user_id):
    return query("SELECT * FROM files WHERE user_id=%s AND is_starred=1 ORDER BY updated_at DESC", (user_id,))

def get_recent_files(user_id, limit=10):
    return query("SELECT * FROM files WHERE user_id=%s ORDER BY updated_at DESC LIMIT %s", (user_id, limit))

def get_file_by_id(file_id, user_id):
    return query("SELECT * FROM files WHERE id=%s AND user_id=%s", (file_id, user_id), one=True)

def create_file_record(user_id, folder_id, name, original_name, object_key, size, mime_type, file_type):
    return execute(
        """INSERT INTO files (user_id, folder_id, name, original_name, object_key, size, mime_type, file_type)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (user_id, folder_id, name, original_name, object_key, size, mime_type, file_type)
    )

def rename_file(file_id, user_id, new_name):
    execute("UPDATE files SET name=%s WHERE id=%s AND user_id=%s", (new_name, file_id, user_id))

def move_file(file_id, user_id, new_folder_id):
    execute("UPDATE files SET folder_id=%s WHERE id=%s AND user_id=%s",
            (new_folder_id if new_folder_id else None, file_id, user_id))

def toggle_star(file_id, user_id):
    execute("UPDATE files SET is_starred=NOT is_starred WHERE id=%s AND user_id=%s", (file_id, user_id))
    f = query("SELECT is_starred FROM files WHERE id=%s", (file_id,), one=True)
    return f['is_starred'] if f else 0

def delete_file_record(file_id, user_id):
    f = get_file_by_id(file_id, user_id)
    if not f:
        return None
    minio_service.delete_file(f['object_key'])
    execute("DELETE FROM files WHERE id=%s AND user_id=%s", (file_id, user_id))
    return f['size']

def generate_share_token(file_id, user_id):
    token = secrets.token_urlsafe(32)
    execute("UPDATE files SET is_shared=1, share_token=%s WHERE id=%s AND user_id=%s",
            (token, file_id, user_id))
    return token

def unshare_file(file_id, user_id):
    execute("UPDATE files SET is_shared=0, share_token=NULL WHERE id=%s AND user_id=%s",
            (file_id, user_id))

def get_file_by_share_token(token):
    return query("SELECT * FROM files WHERE share_token=%s AND is_shared=1", (token,), one=True)

def increment_download(file_id):
    execute("UPDATE files SET download_count=download_count+1 WHERE id=%s", (file_id,))

# Folder operations
def get_folders(user_id, parent_id=None):
    if parent_id is None:
        return query("SELECT * FROM folders WHERE user_id=%s AND parent_id IS NULL ORDER BY name", (user_id,))
    return query("SELECT * FROM folders WHERE user_id=%s AND parent_id=%s ORDER BY name", (user_id, parent_id))

def get_folder_by_id(folder_id, user_id):
    return query("SELECT * FROM folders WHERE id=%s AND user_id=%s", (folder_id, user_id), one=True)

def create_folder(user_id, name, parent_id=None, color='#6366f1'):
    return execute(
        "INSERT INTO folders (user_id, parent_id, name, color) VALUES (%s, %s, %s, %s)",
        (user_id, parent_id, name, color)
    )

def rename_folder(folder_id, user_id, new_name):
    execute("UPDATE folders SET name=%s WHERE id=%s AND user_id=%s", (new_name, folder_id, user_id))

def delete_folder_recursive(folder_id, user_id):
    # Get all sub-folders
    subs = query("SELECT id FROM folders WHERE parent_id=%s AND user_id=%s", (folder_id, user_id))
    for sub in subs:
        delete_folder_recursive(sub['id'], user_id)
    # Delete files in this folder
    files = query("SELECT id FROM files WHERE folder_id=%s AND user_id=%s", (folder_id, user_id))
    total_size = 0
    for f in files:
        size = delete_file_record(f['id'], user_id)
        if size:
            total_size += size
    execute("DELETE FROM folders WHERE id=%s AND user_id=%s", (folder_id, user_id))
    return total_size

def get_breadcrumb(folder_id, user_id):
    path = []
    fid = folder_id
    while fid:
        folder = get_folder_by_id(fid, user_id)
        if not folder:
            break
        path.insert(0, folder)
        fid = folder.get('parent_id')
    return path

def get_folder_stats(user_id):
    result = query("SELECT COUNT(*) as cnt FROM folders WHERE user_id=%s", (user_id,), one=True)
    return result['cnt'] if result else 0

def get_storage_by_type(user_id):
    rows = query(
        "SELECT file_type, SUM(size) as total FROM files WHERE user_id=%s GROUP BY file_type",
        (user_id,)
    )
    return {r['file_type']: r['total'] for r in rows} if rows else {}
