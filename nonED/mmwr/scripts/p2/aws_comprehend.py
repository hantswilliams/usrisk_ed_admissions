import pandas as pd 
import requests
import boto3 
import uuid
from decimal import Decimal
import os 
import json
import dotenv

dotenv.load_dotenv()

boto3.setup_default_session(profile_name='nhit')

medicalComprehend = boto3.client('comprehendmedical', 
                                 region_name='us-east-1')

dynamodb = boto3.resource('dynamodb', 
                            region_name='us-east-1')


# Read in the data
df_htmls = pd.read_csv('nonED/mmwr/data/files/p1B/html_links_data.csv')

# create a uniqid for each row called articleID 
df_htmls['articleID'] = [str(uuid.uuid4()) for _ in range(len(df_htmls))]

#### CLEANING FOR AWS COMPREHEND MEDICAL ####
# get a UTF-8 version of the text column
df_htmls['text_bytes'] = df_htmls['text'].str.len()
df_htmls['text_bytes_flag'] = df_htmls['text_bytes'] > 20000
df_htmls['text_bytes_flag'].value_counts()

## for right now, just keep first 19,999 characters if the text_utf8_bytes is > 20k bytes
for i in range(0, len(df_htmls)):
    if df_htmls['text_bytes_flag'][i] == True:
        df_htmls['text'][i] = df_htmls['text'][i][:19999]
        print('Completed ' + str(i) + ' of ' + str(len(df_htmls)) + ' rows')
    else:
        pass


## create a new column called comprehend_medical
df_htmls['comprehend_medical'] = ''


## loop through each row and get the comprehend medical results, saving them to the comprehend_medical column 
## and also saving a local json file with the results, the name of the file is the articleID
for i in range(0, len(df_htmls)):
    print(i)
    print(df_htmls['articleID'][i])
    print('\n\n')
    try:
        df_htmls['comprehend_medical'][i] = medicalComprehend.detect_entities(Text=df_htmls['text'][i])
        try:
            with open('nonED/mmwr/data/files/p2A/comprehend_medical/' + df_htmls['articleID'][i] + '.json', 'w') as outfile:
                json.dump(df_htmls['comprehend_medical'][i], outfile)
        except:
            print('Failed to save json file for ' + df_htmls['articleID'][i])
    except:
        print('Failed to get comprehend medical for ' + df_htmls['articleID'][i])
    print('Completed ' + str(i) + ' of ' + str(len(df_htmls)) + ' rows')


## save df_htmls to p2A folder
df_htmls.to_csv('nonED/mmwr/data/files/p2A/html_links_data_json.csv', index=False)

# ## save df_htmls to dynamodb
# table = dynamodb.Table('cdc_mmwr')
# with table.batch_writer() as batch:
#     for i in range(0, len(df_htmls)):
#         item = {
#             'articleID': df_htmls['articleID'][i],
#             'comprehend_medical': df_htmls['comprehend_medical'][i],
#         }
#         try:
#             batch.put_item(Item=item)
#             print('Completed ' + str(i) + ' of ' + str(len(df_htmls)) + ' rows')
#         except:
#             print('Failed to save ' + df_htmls['articleID'][i])
#             pass


