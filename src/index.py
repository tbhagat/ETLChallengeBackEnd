import pandas as pd
import json
import boto3

def handler(event, context):

    nyt_source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    jh_source_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

    nyt_df = pd.read_csv(nyt_source_url)
    nyt_df['date'] = pd.to_datetime(nyt_df['date']).dt.strftime('%m/%d/%Y')
    nyt_df.rename(columns={"date": "Date", "cases": "Cases", "deaths": "Deaths"}, inplace=True)
    nyt_df_final= nyt_df.drop(0).reset_index(drop=True)

    jh_df = pd.read_csv(jh_source_url)
    jh_df['Date'] = pd.to_datetime(jh_df['Date']).dt.strftime('%m/%d/%Y')
    jh_df_us = jh_df.loc[jh_df['Country/Region'] == "US"]
    jh_df_final = jh_df_us[["Recovered"]].astype(int).reset_index(drop=True)

    data = nyt_df_final.join(jh_df_final)
    final_data = data.to_json()
    return final_data


    client = boto3.resource('dynamodb')
    table = client.Table("ETLDynamoDB")
    table.put_item(Item= {'Date': '34','company':  'microsoft'})
