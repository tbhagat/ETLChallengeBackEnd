# transform.py
import sys
import pandas as pd
from lib import extract
nyt_df, jh_df = extract.data_pull()


#Transforming data from source
def data_transform():
    try:
        nyt_df.rename(columns={"date": "Date", "cases": "Cases", "deaths": "Deaths"}, inplace=True)
        nyt_df["Date"] = pd.to_datetime(nyt_df["Date"]).dt.strftime('%Y-%m-%d')
        nyt_df_final= nyt_df.drop(0).reset_index(drop=True)

        jh_df.rename(columns={"date": "Date", "recovered": "Recovered"}, inplace=True)
        jh_df["Date"] = pd.to_datetime(jh_df["Date"]).dt.strftime('%Y-%m-%d')
        jh_df.Recovered = jh_df.Recovered.values[::-1]
        jh_df2 = jh_df.drop([0,1,2,3,4,5,6,7,8]).reset_index(drop=True)
        jh_df_final = jh_df2[["Recovered"]].fillna(0).astype(int).reset_index(drop=True)

        data = nyt_df_final.join(jh_df_final)
        fdata = data.to_dict()
        return fdata


    except:
        message = "Error transforming data"
        extract.send_sns(message)
        print(message)
        sys.exit(1)

#Validating transformed data for correct format
def data_validation(fdata):
    for i in fdata["Cases"]:
        if type(fdata["Cases"][i]) == int and fdata["Cases"][i] >= 0:
            pass
        else:
            message = "Cases {} is not in the correct format".format(fdata["Cases"][i])
            extract.send_sns(message)
            print(message)
            sys.exit(1)
    for i in fdata["Deaths"]:
        if type(fdata["Deaths"][i]) == int and fdata["Deaths"][i] >= 0:
            pass
        else:
            message =  "Deaths {} is not in the correct format".format(fdata["Deaths"][i])
            extract.send_sns(message)
            print(message)
            sys.exit(1)
    for i in fdata["Recovered"]:
        if type(fdata["Recovered"][i]) == int and fdata["Recovered"][i] >= 0:
            pass
        else:
            message =  "Recovered {} is not in the correct format".format(fdata["Recovered"][i])
            extract.send_sns(message)
            print(message)
            sys.exit(1)
    for i in fdata["Date"]:
        if type(fdata["Date"][i]) == str:
            pass
        else:
            message = "{} is not in the correct format".format(fdata["Date"][i])
            extract.send_sns(message)
            print(message)
            sys.exit(1)
