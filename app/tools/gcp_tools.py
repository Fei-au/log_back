from google.cloud import storage
from google import genai
from datetime import datetime, timedelta
from pytz import utc
from app.core.config import settings



storage_client = storage.Client()
genai_client = genai.Client(api_key=settings.genai_api_key)

def get_bucket():
    bucket = storage_client.bucket("rtmedia")
    return bucket

def generate_refund_file_name(invoice_number, refund_id, name):
    current_time = datetime.now(tz=utc)
    full_path = f"refund/{current_time.strftime('%Y-%m-%d')}/{invoice_number}-{refund_id}"
    if name:
        full_path += f"-{name}"
    full_path += ".pdf"
    return full_path

def generate_refund_export_csv_name():
    current_time = datetime.now(tz=utc)
    return f"refund/exported_history/{current_time.strftime('%Y%m%d_%H%M%S')}.csv"

def upload_blob(file_bytes, content_type, destination_blob_name):
    bucket = get_bucket()
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0
    blob.upload_from_string(file_bytes, content_type=content_type, if_generation_match=generation_match_precondition)
    return destination_blob_name

def generate_signed_url(refund_invoice_path):
    bucket = get_bucket()
    blob = bucket.blob(refund_invoice_path)
    signed_url = blob.generate_signed_url(expiration=timedelta(hours=1))
    return signed_url


def test_ai_response(description: str):
    from pydantic import BaseModel
    import enum

    class ProductCategory(enum.Enum):
        CLOTHING="Clothing"
        AUTO_PARTS="Auto parts"
        LIGHTING_FIXTURES="Lighting fixtures"
        PET_SUPPLIES="Pet supplies"
        HEALTH_SUPPLEMENTS="Health supplements"
        MASSAGE_CHAIR="Massage chair"
        OTHER="Other"
        
    content = f"""
You are a product categorization AI that categorizes products into one of these strict categories:
- CLOTHING: Apparel items like shirts, pants, dresses, shoes, etc.
- AUTO_PARTS: Components for vehicles like brakes, filters, engine parts, etc.
- LIGHTING_FIXTURES: Lamps, chandeliers, ceiling lights, etc.
- PET_SUPPLIES: Food, toys, beds, or other items for pets.
- HEALTH_SUPPLEMENTS: Vitamins, minerals, protein powders, etc.
- MASSAGE_CHAIR: Only complete massage chairs, not accessories or other furniture.
- OTHER: If the product does not clearly and definitively fit into one of the categories above, you MUST categorize it as "OTHER".

Instructions:
1. First, analyze the product description and determine if it is a definite and unambiguous match for one of the specific categories.
2. If the product is a clear match, return that category.
3. If there is any uncertainty, ambiguity, or the product is not a perfect fit, you must immediately return "OTHER".

Here are a few examples to guide your response:
Product description: "Men's running shoes with ergonomic design"
Category: CLOTHING

Product description: "Dog food dispenser with automatic timer"
Category: PET_SUPPLIES

Product description: "120-count Vitamin C tablets"
Category: HEALTH_SUPPLEMENTS

Product description: "4-pack of replacement brake pads for Ford F-150"
Category: AUTO_PARTS

Product description: "LED desk lamp with adjustable brightness"
Category: LIGHTING_FIXTURES

Product description: "Full-body shiatsu massage chair with heating function"
Category: MASSAGE_CHAIR

Product description: "A comfortable leather recliner chair for living room"
Category: OTHER

Product description: "Replacement pillow for a massage chair"
Category: OTHER

Product description: "A digital thermometer for home use"
Category: OTHER

Product description to categorize: {description}
Category:
"""
    print(content)
    response = genai_client.models.generate_content(
        model='gemini-2.5-pro',
        contents=content,
        config={
            'response_mime_type': 'text/x.enum',
            'response_schema': ProductCategory,
            'temperature': 0.1,  # Low temperature for more deterministic results
            # You can also add other parameters like:
            # 'top_k': 1,  # Limit to only the most likely token
            # 'top_p': 0.95,  # Nucleus sampling parameter
            # 'max_output_tokens': 1,  # Limit output length
        },
    )
    # Use the response as a JSON string.
    return response.text