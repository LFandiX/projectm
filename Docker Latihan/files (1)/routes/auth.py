from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services import auth_service
import re

bp = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        
        errors = []
        if not username or len(username) < 3:
            errors.append('Username minimal 3 karakter.')
        if not is_valid_email(email):
            errors.append('Format email tidak valid.')
        if len(password) < 8:
            errors.append('Password minimal 8 karakter.')
        if password != confirm:
            errors.append('Password tidak cocok.')
        if auth_service.get_user_by_email(email):
            errors.append('Email sudah terdaftar.')
        if auth_service.get_user_by_username(username):
            errors.append('Username sudah digunakan.')
        
        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('auth/register.html', username=username, email=email)
        
        try:
            user_id = auth_service.create_user(username, email, password)
            auth_service.log_activity(user_id, 'register', 'user', user_id, username, request.remote_addr)
            flash('Akun berhasil dibuat! Silakan login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Terjadi kesalahan saat mendaftar. Coba lagi.', 'error')
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = auth_service.authenticate_user(email, password)
        if user:
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            auth_service.log_activity(user['id'], 'login', 'user', user['id'], user['username'], request.remote_addr)
            flash(f'Selamat datang kembali, {user["username"]}!', 'success')
            next_url = request.args.get('next', url_for('dashboard.index'))
            return redirect(next_url)
        else:
            flash('Email atau password salah.', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        auth_service.log_activity(user_id, 'logout', 'user', user_id)
    session.clear()
    flash('Berhasil logout.', 'info')
    return redirect(url_for('auth.login'))
