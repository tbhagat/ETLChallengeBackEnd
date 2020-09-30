# extract.py
import pandas as pd
import boto3
import os
import sys

sns_arn = os.environ['SNS_TOPIC_ARN']
nyt_source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
jh_source_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

def send_sns(text):
    sns = boto3.client('sns')
    try:
        sns.publish(
            TopicArn=sns_arn,
            Subject=("AWS LAMBDA NOTIFICATION"),
            Message=text,
        )
    except:
        print("Cannot send message")




def data_pull():
    try:
        nyt_df = pd.read_csv(nyt_source_url, low_memory=False)
        jh_df =  pd.read_csv(jh_source_url, low_memory=False)
        return nyt_df, jh_df
    except:
        send_sns("Cannot load source data")
        print("Cannot load source data")
        sys.exit(1)
