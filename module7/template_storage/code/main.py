import os
import tempfile # To create a temporary resized file before uploading
from google.cloud import storage
from wand.image import Image  # To resize image
# Add any imports that you may need, but make sure to update requirements.txt

def resize_image_storage(data, context):
    bucket_name = os.environ.get('TRIGGER_BUCKET')
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # Parse file name
    filename = data['name']
    if not ('resized_' in filename):
        # Get the file that has been uploaded to GCS
        blob = bucket.get_blob(filename)
        imagedata = blob.download_as_string()

        # Create a new image object and resample it
        newimage = Image(blob=imagedata)
        newimage.resize(300, 300)

        # Upload the resampled image to the other bucket
        newblob = bucket.blob('resized_' + filename)     
        newblob.upload_from_string(newimage.make_blob())

    return ('', 200)