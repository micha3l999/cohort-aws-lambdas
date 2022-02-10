import boto3
import json


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Cohort-Students')
    response = table.scan()
    items = response.get('Items', [])

    return {
        'statusCode': 200,
        'body': json.dumps(items),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }
