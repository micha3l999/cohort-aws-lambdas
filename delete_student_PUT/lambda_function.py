import boto3
import json


def lambda_handler(event, context):

    # Reading events
    student_id = None
    path_parameters = event.get('pathParameters', [])
    student_id = path_parameters.get('student_id')

    # Return an error message because the student id was not found
    # in Path Parameters
    if not student_id:
        return {
            'statusCode': 400,
            'body': json.dumps('No student id in path parameters')
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Cohort-Students')
    response = table.update_item(
        Key={
            'id': student_id
        },
        UpdateExpression="set #sts=:sta",
        ExpressionAttributeValues={
            ':sta': "inactive",
        },
        ExpressionAttributeNames= {"#sts": "status"},
        ReturnValues="UPDATED_NEW"
    )
    
    # Response for the client
    data = {
        "message": "Student was inactived",
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }

