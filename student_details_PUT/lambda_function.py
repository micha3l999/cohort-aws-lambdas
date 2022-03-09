import boto3
import json
from datetime import date


def lambda_handler(event, context):
    client = boto3.client('lambda')

    body = event.get('body')
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps("Not valid payload")
        }

    # Reading events
    student_payload = json.loads(body)
    path_parameters = event.get('pathParameters', [])
    student_id = None
    student_id = path_parameters.get('student_id')

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

    if not student_id:
        return {
            'statusCode': 400,
            'body': json.dumps("No identification found in path parameters")
        }

    if not student_payload.get('picture'):
        return {
            'statusCode': 400,
            'body': json.dumps("No picture found in payload")
        }

    # Get instance of dynamodb table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Cohort-Students')

    # Check if exists the property to upload and update the user image
    if (student_payload.get('picture_base64')):
        # Upload user picture to s3
        inputParams = {
            "id": student_id,
            "base64_image": student_payload.get('picture_base64')
        }

        # Invoke the lambda to upload the image to s3 and get the image url
        response = client.invoke(
            FunctionName="arn:aws:lambda:us-east-2:001915975023:function:student_picture_PUT",
            InvocationType='RequestResponse',
            Payload=json.dumps(inputParams)
        )

        responseFromLambda = json.load(response["Payload"])
        student_payload["picture"] = responseFromLambda.get("picture_url")

    # Current date to set the update attribute of the item
    today = date.today().strftime("%Y/%m/%d")
    student_payload["updated_at"] = today

    response = table.update_item(
        Key={
            'id': student_id
        },
        UpdateExpression=("set first_name=:fn, last_name=:ln, picture=:pct, age=:ag, "
                          "work_experience=:wrke, years_experience=:yrse, tech_skills=:tchsk, soft_skills=:sfsk, description=:dsc, "
                          "observations=:obs, updated_at=:updt"),
        ExpressionAttributeValues={
            ':fn': student_payload.get('first_name', ""),
            ':ln': student_payload.get('last_name', ""),
            ':pct': student_payload.get('picture', ""),
            ':ag': student_payload.get('age', ""),
            ':wrke': student_payload.get('work_experience', ""),
            ':yrse': student_payload.get('years_experience', ""),
            ':tchsk': student_payload.get('tech_skills', ""),
            ':sfsk': student_payload.get('soft_skills', ""),
            ':dsc': student_payload.get('description', ""),
            ':obs': student_payload.get('observations', ""),
            ':updt': student_payload.get('updated_at', ""),
        },
        ReturnValues="UPDATED_NEW"
    )

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
