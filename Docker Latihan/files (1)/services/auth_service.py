from werkzeug.security import generate_password_hash, check_password_hash
from services.db import query, execute
import logging

logger = logging.getLogger(__name__)

def create_user(username, email, password):
    hashed = generate_password_hash(password)
    try:
        user_id = execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        return user_id
    except Exception as e:
        logger.error(f"Create user error: {e}")
        raise e

def authenticate_user(email, password):
    user = query("SELECT * FROM users WHERE email=%s AND is_active=1", (email,), one=True)
    if user and check_password_hash(user['password'], password):
        return user
    return None

def get_user_by_id(user_id):
    return query("SELECT * FROM users WHERE id=%s", (user_id,), one=True)

def get_user_by_email(email):
    return query("SELECT * FROM users WHERE email=%s", (email,), one=True)

def get_user_by_username(username):
    return query("SELECT * FROM users WHERE username=%s", (username,), one=True)

def update_user_storage(user_id, delta_bytes):
    execute(
        "UPDATE users SET storage_used = GREATEST(0, storage_used + %s) WHERE id=%s",
        (delta_bytes, user_id)
    )

def update_password(user_id, new_password):
    hashed = generate_password_hash(new_password)
    execute("UPDATE users SET password=%s WHERE id=%s", (hashed, user_id))

def log_activity(user_id, action, target_type, target_id=None, target_name=None, ip=None):
    try:
        execute(
            "INSERT INTO activity_log (user_id, action, target_type, target_id, target_name, ip_address) VALUES (%s,%s,%s,%s,%s,%s)",
            (user_id, action, target_type, target_id, target_name, ip)
        )
    except Exception as e:
        logger.warning(f"Log activity error: {e}")
