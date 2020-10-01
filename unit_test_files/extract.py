# extract.py
import pandas as pd
import boto3
import os
import sys

nyt_source_url = "nyt_testdata.csv"
jh_source_url = "jh_testdata.csv"



def data_pull():
    try:
        nyt_df = pd.read_csv(nyt_source_url, low_memory=False)
        jh_df =  pd.read_csv(jh_source_url, low_memory=False)
        return nyt_df, jh_df
    except:
        print("Cannot load source data")
        sys.exit(1)
