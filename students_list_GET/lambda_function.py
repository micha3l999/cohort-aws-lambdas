import boto3
import json
import json_decoder
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):

    # Get the body from event
    query_parameters = event.get("queryStringParameters")

    if not query_parameters:
        return {
            "statusCode": 400,
            "body": json.dumps("Not valid query parameters")
        }

    items_limit = query_parameters.get("itemsLimit")
    last_key = query_parameters.get("last", None)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Cohort-Students')

    if not last_key:
        response = table.query(
            IndexName="status-updated_at-index",
            KeyConditionExpression=Key('status').eq("active"),
            Limit=int(items_limit)
        )
    else:
        response = table.query(
            IndexName="status-updated_at-index",
            KeyConditionExpression=Key('status').eq("active"),
            Limit=int(items_limit),
            ExclusiveStartKey=json.loads(last_key)
        )

    data = {
        "items": response.get('Items', []),
        "lastEvaluatedKey": response.get('LastEvaluatedKey', None)
    }

    return {
        'statusCode': 200,
        'body': json.dumps(data, cls=json_decoder.DecimalEncoder),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }
