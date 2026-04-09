import mysql.connector
from mysql.connector import pooling
from flask import current_app, g
import logging

logger = logging.getLogger(__name__)
_pool = None

def get_pool(app=None):
    global _pool
    if _pool is None:
        cfg = app.config if app else current_app.config
        _pool = pooling.MySQLConnectionPool(
            pool_name="fileshare_pool",
            pool_size=10,
            host=cfg['DB_HOST'],
            port=cfg['DB_PORT'],
            user=cfg['DB_USER'],
            password=cfg['DB_PASSWORD'],
            database=cfg['DB_NAME'],
            autocommit=False,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
        )
    return _pool

def get_db():
    if 'db' not in g:
        g.db = get_pool().get_connection()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        try:
            db.close()
        except Exception:
            pass

def query(sql, args=(), one=False, commit=False):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(sql, args)
        if commit:
            db.commit()
            return cursor.lastrowid
        rv = cursor.fetchone() if one else cursor.fetchall()
        return rv
    except Exception as e:
        if commit:
            db.rollback()
        raise e
    finally:
        cursor.close()

def execute(sql, args=()):
    return query(sql, args, commit=True)

def init_db(app):
    with app.app_context():
        db = get_pool(app).get_connection()
        cursor = db.cursor()
        statements = [
            """CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                avatar VARCHAR(255) DEFAULT NULL,
                storage_used BIGINT DEFAULT 0,
                storage_quota BIGINT DEFAULT 10737418240,
                is_active TINYINT(1) DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
            """CREATE TABLE IF NOT EXISTS folders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                parent_id INT DEFAULT NULL,
                name VARCHAR(255) NOT NULL,
                color VARCHAR(20) DEFAULT '#6366f1',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (parent_id) REFERENCES folders(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
            """CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                folder_id INT DEFAULT NULL,
                name VARCHAR(255) NOT NULL,
                original_name VARCHAR(255) NOT NULL,
                object_key VARCHAR(512) NOT NULL,
                size BIGINT NOT NULL DEFAULT 0,
                mime_type VARCHAR(128) DEFAULT 'application/octet-stream',
                file_type VARCHAR(50) DEFAULT 'other',
                is_starred TINYINT(1) DEFAULT 0,
                is_shared TINYINT(1) DEFAULT 0,
                share_token VARCHAR(64) DEFAULT NULL,
                download_count INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
            """CREATE TABLE IF NOT EXISTS activity_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                action VARCHAR(50) NOT NULL,
                target_type VARCHAR(20) NOT NULL,
                target_id INT,
                target_name VARCHAR(255),
                ip_address VARCHAR(45),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"""
        ]
        for stmt in statements:
            cursor.execute(stmt)
        db.commit()
        cursor.close()
        db.close()
        logger.info("Database initialized successfully")
