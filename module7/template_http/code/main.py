import os
import tempfile    # To create temporary file before uploading to bucket
from google.cloud import storage
from flask import escape
# Add any imports that you may need, but make sure to update requirements.txt

def create_file_http(request):
    body = request.get_json()
    fileid = body["fileid"]

    bucket_name = os.environ.get('BUCKET_NAME')
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    file = bucket.blob(fileid)
    file.upload_from_string('')

    response = ""
    return response, 200
