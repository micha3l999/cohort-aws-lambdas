import boto3
import json
import uuid


def lambda_handler(event, context):

    # Reading `body` from event
    body = event.get('body')
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps("Not valid payload")
        }

    student_payload = json.loads(body)
    student_payload["id"] = str(uuid.uuid4())

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

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CohortStudents')
    response = table.put_item(
        Item=student_payload
    )
    print(response)

    # Response for the client
    data = {
        "message": "Student was created",
        "student_created": student_payload
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True
        },
    }
