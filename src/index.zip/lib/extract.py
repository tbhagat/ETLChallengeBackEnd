# extract.py
import pandas as pd

nyt_source_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
jh_source_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"


def nyt_pull():
    nyt = pd.read_csv(nyt_source_url, low_memory=False)
    return (nyt)

def jh_pull():
    jh =  pd.read_csv(jh_source_url, low_memory=False)
    return jh
