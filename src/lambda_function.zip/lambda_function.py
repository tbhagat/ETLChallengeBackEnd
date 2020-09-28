import json
import boto3
from decimal import Decimal


client = boto3.resource('dynamodb')
table = client.Table("ETLBackend-Table-GF6RYJTLM6Q3")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    resp = table.scan()
    return{
        'statusCode': 200,
        'body': json.dumps(resp["Items"], cls=DecimalEncoder),
        'headers': {
		"Access-Control-Allow-Origin": "*"
	    }
    }
