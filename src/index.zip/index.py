import pandas as pd
import json
import boto3
import os
from lib import extract

def handler(event, context):
    extract.sum()
    nyt_source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    jh_source_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

    nyt_df = pd.read_csv(nyt_source_url, low_memory=False)
    nyt_df.rename(columns={"date": "Date", "cases": "Cases", "deaths": "Deaths"}, inplace=True)
    nyt_df_final= nyt_df.drop(0).reset_index(drop=True)

    jh_df = pd.read_csv(jh_source_url, low_memory=False)
    jh_df_us = jh_df.loc[jh_df['Country/Region'] == "US"]
    jh_df_final = jh_df_us[["Recovered"]].astype(int).reset_index(drop=True)

    data = nyt_df_final.join(jh_df_final)
    fdata = data.to_dict()

    client = boto3.resource('dynamodb')
    table = client.Table(os.environ['TABLE_NAME'])
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
    sns_arn = os.environ['SNS_TOPIC_ARN']
    sns = boto3.client("sns")

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
