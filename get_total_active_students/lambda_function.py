import boto3
import botocore
import json
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    # Reading body from event

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Cohort-Students")

    response = table.query(
        IndexName="status-updated_at-index",
        KeyConditionExpression=Key('status').eq("active"),
        ProjectionExpression="id"
    )

    total_students = response.get("Count")

    data = {
        "message": "Total items successfully retrieved",
        "count": total_students,
    }
    return {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
    }
