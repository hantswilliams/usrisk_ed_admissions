import pandas as pd
import os
import json
import streamlit as st

## load data
df = pd.read_csv('nonED/mmwr/data/files/p3/comprehend_medical_entities.csv')
df['dateline'] = pd.to_datetime(df['dateline'], format='%Y-%m-%d')
df['dateMonth'] = df['dateline'].dt.strftime('%Y-%m')

## get value counts where entity_type is == DX_NAME, all time 
total_counts = df[df['entity_type'] == 'DX_NAME'].value_counts('entity_text')
total_counts.head(10)

## create frequency table where the columns are dateMonth, rows are entity_text where entity_type == DX_NAME, and values are the count of entity_text
df_freq = df[df['entity_type'] == 'DX_NAME'].groupby(['dateMonth', 'entity_text']).size().reset_index(name='count')
df_freq = df_freq.sort_values(['count', 'entity_text'], ascending=[False, True])

## create streamlit app 
st.title('MMWR CDC Fast Analaysis')
st.sidebar.title('Filters')
st.sidebar.markdown('Select filters to update the data.')

## create sidebar filters
## date range
date_range = st.sidebar.slider('Date Range', min(df['dateline']).date(), max(df['dateline']).date(), (min(df['dateline']).date(), max(df['dateline']).date()))

## entity type
entity_type = st.sidebar.selectbox('Entity Type', df['entity_type'].unique())

## entity text
entity_text = st.sidebar.selectbox('Entity Text', df[df['entity_type'] == entity_type]['entity_text'].unique())

## create dataframe based on filters
df_filtered = df[(df['dateline'] >= date_range[0]) & (df['dateline'] <= date_range[1]) & (df['entity_type'] == entity_type) & (df['entity_text'] == entity_text)]

## create dataframe for frequency table
df_freq_filtered = df_freq[(df_freq['dateMonth'] >= date_range[0].strftime('%Y-%m')) & (df_freq['dateMonth'] <= date_range[1].strftime('%Y-%m')) & (df_freq['entity_text'] == entity_text)]

## create dataframe for total counts
total_counts_filtered = total_counts[total_counts.index == entity_text]

## create dataframe for total counts by month
total_counts_by_month = df[df['entity_type'] == 'DX_NAME'].groupby(['dateMonth']).size().reset_index(name='count')

## create dataframe for total counts by month filtered
total_counts_by_month_filtered = total_counts_by_month[(total_counts_by_month['dateMonth'] >= date_range[0].strftime('%Y-%m')) & (total_counts_by_month['dateMonth'] <= date_range[1].strftime('%Y-%m'))]

## create dataframe for total counts by month filtered
total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'count': 'total_count'})

## merge total counts by month filtered into df_freq_filtered
df_freq_filtered = df_freq_filtered.merge(total_counts_by_month_filtered, on='dateMonth', how='left')

## create dataframe for total counts by month filtered
total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'total_count': 'total_count_by_month'})

## create dataframe for total counts by month filtered
total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'total_count_by_month': 'total_count'})

## create dataframe for total counts by month filtered
total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'total_count': 'total_count_by_month'})

## merge total counts by month filtered into df_freq_filtered
df_freq_filtered = df_freq_filtered.merge(total_counts_by_month_filtered, on='dateMonth', how='left')


## display total counts
st.write('Total Counts: ' + str(total_counts_filtered.values[0]))

## display total counts by month
st.write('Total Counts by Month: ')
st.write(total_counts_by_month_filtered)

## display frequency table
st.write('Frequency Table: ')
st.write(df_freq_filtered)

## display dataframe
st.write('Dataframe: ')
st.write(df_filtered)

## display total counts
st.write('Total Counts: ' + str(total_counts_filtered.values[0]))

## display total counts by month
st.write('Total Counts by Month: ')
st.write(total_counts_by_month_filtered)

## display frequency table
st.write('Frequency Table: ')
st.write(df_freq_filtered)