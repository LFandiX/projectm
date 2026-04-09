import os
import boto3
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_pos_key"

# Konfigurasi S3 / MinIO
s3_client = boto3.client(
    's3',
    endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT')}",
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY'),
    region_name='us-east-1'
)

BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')

@app.route('/')
def index():
    # Mengambil daftar object dari bucket
    images = []
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            for obj in response['Contents']:
                # Generate URL yang berlaku selama 1 jam untuk preview
                url = s3_client.generate_presigned_url('get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']},
                    ExpiresIn=3600)
                images.append({'name': obj['Key'], 'url': url})
    except Exception as e:
        flash(f"Gagal mengambil data: {str(e)}")

    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file_upload')
    if file and file.filename != '':
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename, 
                                 ExtraArgs={'ContentType': file.content_type})
        flash('Upload berhasil!')
    return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
        flash(f'File {filename} berhasil dihapus!')
    except Exception as e:
        flash(f'Gagal menghapus: {str(e)}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)