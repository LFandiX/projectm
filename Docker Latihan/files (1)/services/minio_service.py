from minio import Minio
from minio.error import S3Error
from flask import current_app
import uuid, io, logging
from datetime import timedelta

logger = logging.getLogger(__name__)
_client = None

def get_client():
    global _client
    if _client is None:
        cfg = current_app.config
        _client = Minio(
            cfg['MINIO_ENDPOINT'],
            access_key=cfg['MINIO_ACCESS_KEY'],
            secret_key=cfg['MINIO_SECRET_KEY'],
            secure=cfg['MINIO_SECURE'],
        )
        bucket = cfg['MINIO_BUCKET']
        if not _client.bucket_exists(bucket):
            _client.make_bucket(bucket)
            logger.info(f"Created MinIO bucket: {bucket}")
    return _client

def upload_file(file_obj, object_key, content_type, size):
    client = get_client()
    bucket = current_app.config['MINIO_BUCKET']
    client.put_object(
        bucket, object_key, file_obj, size,
        content_type=content_type
    )
    return object_key

def get_presigned_url(object_key, expires_hours=1):
    client = get_client()
    bucket = current_app.config['MINIO_BUCKET']
    url = client.presigned_get_object(
        bucket, object_key,
        expires=timedelta(hours=expires_hours)
    )
    return url

def delete_file(object_key):
    try:
        client = get_client()
        bucket = current_app.config['MINIO_BUCKET']
        client.remove_object(bucket, object_key)
        return True
    except S3Error as e:
        logger.error(f"MinIO delete error: {e}")
        return False

def get_file_stream(object_key):
    client = get_client()
    bucket = current_app.config['MINIO_BUCKET']
    response = client.get_object(bucket, object_key)
    return response

def generate_object_key(user_id, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'bin'
    unique = uuid.uuid4().hex
    return f"users/{user_id}/{unique}.{ext}"
