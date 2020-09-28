import pandas as pd
import json
import boto3
from extract.py import *

def handler(event, context):
    TestMe()
    nyt_source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    jh_source_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

    nyt_df = pd.read_csv(nyt_source_url)
    nyt_df.rename(columns={"date": "Date", "cases": "Cases", "deaths": "Deaths"}, inplace=True)
    nyt_df_final= nyt_df.drop(0).reset_index(drop=True)

    jh_df = pd.read_csv(jh_source_url)
    jh_df_us = jh_df.loc[jh_df['Country/Region'] == "US"]
    jh_df_final = jh_df_us[["Recovered"]].astype(int).reset_index(drop=True)

    data = nyt_df_final.join(jh_df_final)
    data["Date"] = pd.to_datetime(data['Date'])
    data["Date"] = data['Date'].dt.date


    final_data = data.to_dict()

    client = boto3.resource('dynamodb')
    table = client.Table("Covid")

    for i in final_data["Date"]:
        table.put_item(Item= {'Date': final_data["Date"][i].isoformat(),
                                "Cases": final_data["Cases"][i],
                                "Deaths": final_data["Deaths"][i],
                                "Recovered": final_data["Recovered"][i]

        })
