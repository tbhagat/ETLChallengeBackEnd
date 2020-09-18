import boto3
import json


def handler(event, context):
    dynamodb = boto3.client('dynamodb')
    dynamodb.update_item(
        TableName='analytics',
        Key={
            'site':{'S':'site'}
        },
        UpdateExpression='Set visits = if_not_exists(visits, :inc)',
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        ReturnValues="UPDATED_NEW"
    )
    response = dynamodb.update_item(
        TableName='analytics',
        Key={
            'site':{'S':'site'}
        },
        UpdateExpression='Set visits = visits + :inc',
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        ReturnValues="UPDATED_NEW"
)
    return{
        'statusCode': 200,
        'body': json.dumps({'visitors': response['Attributes']['visits']['N']}),
        'headers': {
		"Access-Control-Allow-Origin": "*"
	}
}
