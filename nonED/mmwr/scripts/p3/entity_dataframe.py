import pandas as pd
import os
import json

## get files 
files = os.listdir('nonED/mmwr/data/files/p2A/comprehend_medical')

## bring in nonED/mmwr/data/files/p2A/html_links_data_json.csv
meta = pd.read_csv('nonED/mmwr/data/files/p2A/html_links_data_json.csv')
meta = meta.drop(['comprehend_medical', 'text_bytes_flag', 'text_bytes', 'text'], axis=1)
meta['dateline'] = meta['dateline'].str.split('/').str[1]
meta['dateline'] = pd.to_datetime(meta['dateline'].str.strip(), format='%B %d, %Y')

## for each file, read in the json and get the entities
entities = []

for file in files:
    with open('nonED/mmwr/data/files/p2A/comprehend_medical/' + file) as json_file:
        data = json.load(json_file)
        print('Processing ' + file[:-5])
        entities.append(data['Entities'])

for i in range(0, len(entities)):
    for j in range(0, len(entities[i])):
        entities[i][j]['articleID'] = files[i][:-5]

## merge the entities into dataframe
df = []
for i in range(0, len(entities)):
    for j in range(0, len(entities[i])):
        df.append(entities[i][j])

df_entities = pd.DataFrame(df)

## merge the entities into the data dataframe
df_entities = df_entities.rename(columns={'Text': 'entity_text', 'Type': 'entity_type', 'Score': 'entity_score'})
df_entities = df_entities.drop(['BeginOffset', 'EndOffset'], axis=1)
df_entities = df_entities.merge(meta, on='articleID', how='left')

## save the dataframe to a csv
df_entities.to_csv('nonED/mmwr/data/files/p3/comprehend_medical_entities.csv', index=False)
