import pandas as pd
import json
import boto3
import os
from lib import extract
from lib import transform

#Connecting to database
client = boto3.resource('dynamodb')
table = client.Table(os.environ['TABLE_NAME'])


def handler(event, context):

    #Transforming data and validating it's in the correct format
    fdata = transform.data_transform()
    db_data = table.scan(AttributesToGet=['Date'])
    transform.data_validation(fdata)

    #Compiling date list from db
    date_list = []
    for i in db_data["Items"]:
        json_str = json.dumps(i)
        resp_dict = json.loads(json_str)
        date_list.append(resp_dict.get('Date'))

    #Putting new data in db if the specifed date does not already exist in db
    count = 0
    updated_items = []
    try:
        for i in fdata["Date"]:
            if fdata["Date"][i] not in date_list:
                table.put_item(Item= {'Date': fdata["Date"][i],
                                    "Cases": fdata["Cases"][i],
                                    "Deaths": fdata["Deaths"][i],
                                    "Recovered": fdata["Recovered"][i]})
                count +=1
                updated_items.append(("Date {} has been loaded into the database. Cases {},  Deaths {}, Recovered {}".format(fdata["Date"][i],fdata["Cases"][i], fdata["Deaths"][i],  fdata["Recovered"][i])))

        message =  ("{} dates have been added to the database.".format(count) + "\n" + "\n".join(updated_items))

    #Sending SNS notification
        if count > 0:
            extract.send_sns(message)
        else:
            extract.send_sns("There were no database updates with the last ETL run.")
    except:
            message = "Cannot load into database"
            extract.send_sns(message)
            print(message)
            sys.exit(1)
