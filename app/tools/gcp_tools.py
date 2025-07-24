from google.cloud import storage
from datetime import datetime, timedelta
from pytz import utc


storage_client = storage.Client()
def get_bucket():
    bucket = storage_client.bucket("rtmedia")
    return bucket

def generate_blob_name(invoice_number, refund_id, name):
    current_time = datetime.now(tz=utc)
    full_path = f"refund/{current_time.strftime('%Y-%m-%d')}/{invoice_number}-{refund_id}"
    if name:
        full_path += f"-{name}"
    full_path += ".pdf"
    return full_path

def upload_blob(file_bytes, invoice_number, refund_id, name):
    destination_blob_name = generate_blob_name(invoice_number, refund_id, name)
    bucket = get_bucket()
    blob = bucket.blob(destination_blob_name)

    generation_match_precondition = 0

    blob.upload_from_string(file_bytes, content_type="application/pdf", if_generation_match=generation_match_precondition)
    
    print(
        f"File uploaded to {destination_blob_name}."
    )
    return destination_blob_name


def generate_signed_url(refund_invoice_path):
    bucket = get_bucket()
    blob = bucket.blob(refund_invoice_path)
    signed_url = blob.generate_signed_url(expiration=timedelta(hours=1))
    return signed_url