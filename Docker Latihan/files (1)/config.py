import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
    
    # MySQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'fileshare_db')
    
    # MinIO
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'fileshare')
    MINIO_SECURE = os.getenv('MINIO_SECURE', 'False').lower() == 'true'
    
    # Upload
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE_MB', 500)) * 1024 * 1024
    STORAGE_QUOTA_BYTES = int(os.getenv('STORAGE_QUOTA_GB', 10)) * 1024 * 1024 * 1024
    
    ALLOWED_EXTENSIONS = {
        'image': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp', 'bmp', 'ico'],
        'video': ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'],
        'audio': ['mp3', 'wav', 'flac', 'ogg', 'aac', 'm4a'],
        'document': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf', 'odt'],
        'archive': ['zip', 'rar', '7z', 'tar', 'gz', 'bz2'],
        'code': ['py', 'js', 'ts', 'html', 'css', 'json', 'xml', 'yaml', 'yml', 'md', 'sql'],
    }
