import boto3
import json


def lambda_handler(event, context):
    body = event.get('body')
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps("Not valid payload")
        }

    # Reading events
    student_id = None
    path_parameters = event.get('pathParameters', [])
    student_payload = json.loads(body)

    if path_parameters:
        student_id = path_parameters.get('student_id')
        student_payload["id"] = student_id

    # Return an error message because the student id was not found
    # in Path Parameters
    if not student_id:
        return {
            'statusCode': 400,
            'body': json.dumps('No student id in path parameters')
        }

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
    response = table.update_item(
        Key={
            'id': student_id
        },
        UpdateExpression="set first_name=:fn, last_name=:ln",
        ExpressionAttributeValues={
            ':fn': student_payload.get('first_name', ""),
            ':ln': student_payload.get('last_name', "")
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)

    # Response for the client
    data = {
        "message": "Student was updated",
        "student_updated": student_payload
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }

