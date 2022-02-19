import boto3
import json
import json_decoder
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Cohort-Students')
    response = table.query(
        IndexName="status-updated_at-index",
        KeyConditionExpression=Key('status').eq("active")
    )
    items = response.get('Items', [])

    return {
        'statusCode': 200,
        'body': json.dumps(items, cls=json_decoder.DecimalEncoder),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }
