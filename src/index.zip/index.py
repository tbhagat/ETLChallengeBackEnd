import pandas as pd
import json
import boto3
import os
from lib import extract
from lib import transform

client = boto3.resource('dynamodb')
table = client.Table(os.environ['TABLE_NAME'])
sns_arn = os.environ['SNS_TOPIC_ARN']
sns = boto3.client("sns")


def handler(event, context):
    fdata = transform.data_transform()
    db_data = table.scan(AttributesToGet=['Date'])

    date_list = []
    for i in db_data["Items"]:
        json_str = json.dumps(i)
        resp_dict = json.loads(json_str)
        date_list.append(resp_dict.get('Date'))

    count = 0
    updated_items = []
    for i in fdata["Date"]:
        if fdata["Date"][i] not in date_list:
            table.put_item(Item= {'Date': fdata["Date"][i],
                                "Cases": fdata["Cases"][i],
                                "Deaths": fdata["Deaths"][i],
                                "Recovered": fdata["Recovered"][i]})
            count +=1
            updated_items.append(("Date {} has been loaded into the database. Cases {},  Deaths {}, Recovered {}".format(fdata["Date"][i],fdata["Cases"][i], fdata["Deaths"][i],  fdata["Recovered"][i])))

    message =  ("{} dates have been added to the database.".format(count) + "\n" + "\n".join(updated_items))


    if count > 0:
        response = sns.publish(
            TargetArn=sns_arn,
            Subject=("AWS LAMBDA NOTIFICATION"),
            Message=(message))
    else:
        response = sns.publish(
            TargetArn=sns_arn,
            Subject=("AWS LAMBDA NOTIFICATION"),
            Message=("There were no database updates with the last ETL run."))
