# transform.py
import pandas as pd
from lib import extract

nyt = extract.nyt_pull()

def data_transform():
    nyt_df = extract.nyt_pull()
    nyt_df.rename(columns={"date": "Date", "cases": "Cases", "deaths": "Deaths"}, inplace=True)
    nyt_df_final= nyt_df.drop(0).reset_index(drop=True)

    jh_df = extract.jh_pull()
    jh_df_us = jh_df.loc[jh_df['Country/Region'] == "US"]
    jh_df_final = jh_df_us[["Recovered"]].astype(int).reset_index(drop=True)

    data = nyt_df_final.join(jh_df_final)
    fdata = data.to_dict()
    return fdata
