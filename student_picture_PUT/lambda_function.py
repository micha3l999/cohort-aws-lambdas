import boto3
import json
import base64
import imghdr


def lambda_handler(event, context):
    
    # S3 instance and bucke name of s3
    s3 = boto3.resource('s3')
    bucket_name = "cohort-bucket-s3"
    
    # Check image in payload event
    if not event["base64_image"]:
        return {
            "statusCode": 500,
            "image_url": None, 
        }

    if not event["id"]:
        return {
            "statusCode": 500,
            "image_url": None,
        }

    id = event.get("id")
    base64_image = extract_header_base64(event.get("base64_image"))

    picture_decoded = base64.b64decode(base64_image)
    file_name = id

    # Get the image type of the picture decoded
    extension = get_file_extension(file_name, picture_decoded)

    # Upload image to s3
    obj = s3.Object(bucket_name, f"profile_images/{file_name}.{extension}")
    obj.put(
        Body = picture_decoded,
        ACL = 'public-read',
        ContentType = f'image/{extension}'
    )

    # Get bucket location s3
    location = boto3.client("s3").get_bucket_location(
        Bucket = bucket_name
    )["LocationConstraint"]

    # Get object url
    object_url = "https://%s.s3-%s.amazonaws.com/profile_images/%s.%s" % (bucket_name,location, file_name, extension)

    # TODO implement
    return {
        'picture_url': object_url
    }

def get_file_extension(file_name, decoded_file):
    # Get the image extension
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension

def extract_header_base64(data):
    # Check and break out the header from the base64 content
    if 'data:' in data and ';base64,' in data:
        header, data = data.split(';base64,')
    
    return data