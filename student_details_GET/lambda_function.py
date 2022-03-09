import boto3
import json
import json_decoder

def lambda_handler(event, context):
    # Reading events
    student = None
    student_id = None

    path_parameters = event.get('pathParameters')
    if path_parameters:
        student_id = path_parameters.get('student_id')

    # Return an error message because the student id was not found
    # in Path Parameters
    if not student_id:
        return {
            'statusCode': 400,
            'body': json.dumps('No student id in path parameters')
        }

    # Student id was found in Path Parameters, we are going to look up for it in DynamoDB
    if student_id:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Cohort-Students')
        response = table.get_item(
            Key={
                'id': student_id,
            }
        )
        student = response.get('Item', {})

    # Student not found with that `id`, returning an error message
    if not student:
        return {
            'statusCode': 404,
            'body': json.dumps("Student not found")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(student, cls=json_decoder.DecimalEncoder),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }
