import pandas as pd
import os
import json
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

## load data
df = pd.read_csv('/Users/hantswilliams/Documents/development/python_projects/usrisk_ed_admissions/nonED/mmwr/data/files/p3/comprehend_medical_entities.csv')
df['date'] = pd.to_datetime(df['dateline'].str.strip(), format='%Y-%m-%d')
df['dateline'] = pd.to_datetime(df['dateline'], format='%Y-%m-%d')
df['dateMonth'] = df['dateline'].dt.strftime('%Y-%m')

## get value counts where entity_type is == DX_NAME, all time 
total_counts = df[df['entity_type'] == 'DX_NAME'].value_counts('entity_text')
total_counts.head(10)

## create frequency table where the columns are dateMonth, rows are entity_text where entity_type == DX_NAME, and values are the count of entity_text
df_freq = df[df['entity_type'] == 'DX_NAME'].groupby(['dateMonth', 'entity_text']).size().reset_index(name='count')
df_freq = df_freq.sort_values(['count', 'entity_text'], ascending=[False, True])

## create streamlit app 
st.title('MMWR CDC Fast Analysis')
st.sidebar.title('Filters')
st.sidebar.markdown('Select filters to update the data.')

## create sidebar filters
## date range
# Create a date range slider in the sidebar using Streamlit's st.sidebar.slider()
min_date = min(df['date']).date()
max_date = max(df['date']).date()
date_range = st.sidebar.slider('Date Range', min_value=min_date, max_value=max_date, value=(min_date, max_date))

# Convert start_date and end_date to datetime objects
start_date = datetime.combine(date_range[0], datetime.min.time())
end_date = datetime.combine(date_range[1], datetime.max.time())

# # ## entity type
# entity_type = st.sidebar.selectbox('Entity Type', df['entity_type'].unique())

# ## entity text
# entity_text_options = df[df['entity_type'] == entity_type]['entity_text'].unique()
# entity_text_options = ['All'] + list(entity_text_options)
# entity_text = st.sidebar.selectbox('Entity Text', entity_text_options)

# Filter the DataFrame based on the selected date range
filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Display the filtered DataFrame
st.dataframe(filtered_df)






### CHART 1 

# Group the filtered_df by 'dateMonth' and 'entity_type', and calculate the count
grouped_df = filtered_df.groupby(['dateMonth', 'entity_type']).size().reset_index(name='count')

# Pivot the grouped_df to have 'dateMonth' as index, 'entity_type' as columns, and 'count' as values
pivot_df = grouped_df.pivot(index='dateMonth', columns='entity_type', values='count')

# Plot the stacked bar chart using DataFrame.plot.bar(stacked=True)
fig, ax = plt.subplots()
pivot_df.plot.bar(stacked=True, ax=ax)

# Customize the chart
plt.title('Entity Type by Date Month')
plt.xlabel('Date Month')
plt.ylabel('Count')
plt.xticks(rotation=45)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Display the chart in Streamlit
st.pyplot(fig)























st.write('Entity Type')
st.dataframe(filtered_df.value_counts('entity_type'))

st.write('Entity Type by Date Month')
st.dataframe(filtered_df.groupby(['dateMonth', 'entity_type']).size().reset_index(name='count'))






## create a value counts table for entity_text where entity_type = DX_NAME
st.write('Value Counts where entity_type = DX_NAME')
st.dataframe(filtered_df[filtered_df['entity_type'] == 'DX_NAME'].value_counts('entity_text'))

## create a value counts table for entity_text where entity_type = TEST_NAME
st.write('Value Counts where entity_type = TEST_NAME')
st.dataframe(filtered_df[filtered_df['entity_type'] == 'TEST_NAME'].value_counts('entity_text'))












## create dataframe for frequency table
# df_freq_filtered = df_freq[(df_freq['dateMonth'] >= date_range[0].strftime('%Y-%m')) & (df_freq['dateMonth'] <= date_range[1].strftime('%Y-%m')) & (df_freq['entity_text'] == entity_text)]

# ## create dataframe for total counts
# total_counts_filtered = total_counts[total_counts.index == entity_text]

# ## create dataframe for total counts by month
# total_counts_by_month = df[df['entity_type'] == 'DX_NAME'].groupby(['dateMonth']).size().reset_index(name='count')

# ## create dataframe for total counts by month filtered
# total_counts_by_month_filtered = total_counts_by_month[(total_counts_by_month['dateMonth'] >= date_range[0].strftime('%Y-%m')) & (total_counts_by_month['dateMonth'] <= date_range[1].strftime('%Y-%m'))]

# ## create dataframe for total counts by month filtered
# total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'count': 'total_count'})

# ## merge total counts by month filtered into df_freq_filtered
# df_freq_filtered = df_freq_filtered.merge(total_counts_by_month_filtered, on='dateMonth', how='left')

# ## create dataframe for total counts by month filtered
# total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'total_count': 'total_count_by_month'})

# ## create dataframe for total counts by month filtered
# total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'total_count_by_month': 'total_count'})

# ## create dataframe for total counts by month filtered
# total_counts_by_month_filtered = total_counts_by_month_filtered.rename(columns={'total_count': 'total_count_by_month'})

# ## merge total counts by month filtered into df_freq_filtered
# df_freq_filtered = df_freq_filtered.merge(total_counts_by_month_filtered, on='dateMonth', how='left')


# ## display total counts
# st.write('Total Counts: ' + str(total_counts_filtered.values[0]))

# ## display total counts by month
# st.write('Total Counts by Month: ')
# st.write(total_counts_by_month_filtered)

# ## display frequency table
# st.write('Frequency Table: ')
# st.write(df_freq_filtered)

# ## display dataframe
# st.write('Dataframe: ')
# st.write(df_filtered)

# ## display total counts
# st.write('Total Counts: ' + str(total_counts_filtered.values[0]))

# ## display total counts by month
# st.write('Total Counts by Month: ')
# st.write(total_counts_by_month_filtered)

# ## display frequency table
# st.write('Frequency Table: ')
# st.write(df_freq_filtered)