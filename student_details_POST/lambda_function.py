import boto3
import botocore
import json
from datetime import date

# Define the client to interact with AWS Lambda


def lambda_handler(event, context):
    client = boto3.client('lambda')

    # Reading body from event
    body = event.get('body')
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps("Not valid payload")
        }

    student_payload = json.loads(body)

    # Return error messages if the student does not have enough info
    if not student_payload.get('first_name'):
        return {
            'statusCode': 400,
            'body': json.dumps("No first name found in payload")
        }

    if not student_payload.get('last_name'):
        return {
            'statusCode': 400,
            'body': json.dumps("No last name found in payload")
        }

    if not student_payload.get('id'):
        return {
            'statusCode': 400,
            'body': json.dumps("No identification found in payload")
        }

    if not student_payload.get('picture'):
        return {
            'statusCode': 400,
            'body': json.dumps("No picture found in payload")
        }

    # Create the table in the dynamodb
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Cohort-Students')

    user_exists = check_user_created(student_payload.get('id'), table)

    if user_exists:
        return {
            'statusCode': 409,
            'body': json.dumps("Student already exists in our system"),
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
        }

    # Upload user picture to s3
    inputParams = {
        "id": student_payload.get('id'),
        "base64_image": student_payload.get('picture')
    }

    # Invoke the lambda to upload the image to s3 and get the image url
    response = client.invoke(
        FunctionName="arn:aws:lambda:us-east-2:001915975023:function:student_picture_PUT",
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )

    responseFromLambda = json.load(response["Payload"])
    student_payload["picture"] = responseFromLambda.get("picture_url")

    # Creating default values for the user
    student_payload["status"] = "active"

    today = date.today().strftime("%Y/%m/%d")
    student_payload["created_at"] = today
    student_payload["updated_at"] = today

    already_exists = False
    try:
        response = table.put_item(
            Item=student_payload,
            ConditionExpression='attribute_not_exists(id)',
        )

    except botocore.exceptions.ClientError as e:
        # Ignore the ConditionalCheckFailedException, bubble up
        # other exceptions.
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        already_exists = True

    # If student exists return an error message
    if already_exists:
        return {
            'statusCode': 409,
            'body': json.dumps("Student already exists in our system"),
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
        }

    # Response for the client
    data = {
        "message": "Student was created",
        "student_created": student_payload,
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }


def check_user_created(id, table):

    # Searching user in database
    response = table.get_item(
        Key={
            'id': id
        }
    )

    user = response.get('Item', {})

    return user
