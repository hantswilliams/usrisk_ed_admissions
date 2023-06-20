import requests
import pandas as pd
import bs4  # BeautifulSoup4

df_htmls = pd.read_csv('nonED/mmwr/data/files/p1A/html_links.csv')

# a function that captures the div class="dateline" and the <p> tags inside of it
def get_dateline(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    dateline = soup.select('div.dateline')
    ## if dateline is empty, then return empty string
    if len(dateline) == 0:
        return ''
    else:
        dateline = [d.getText() for d in dateline]
        dateline = '\n'.join(dateline)
        return dateline

# a function that has an inpute of a url, and then keeps on the <p> tags and <h> tags
def get_text(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    text = soup.select('p, h1, h2, h3, h4, h5, h6')
    text = [t.getText() for t in text]
    text = '\n'.join(text)
    return text


# ## quick tests
# sample = df_htmls['link'][0]
# get_dateline(sample)
# get_text(sample)


## create two new blank columns, dateline and text
df_htmls['dateline'] = ''
df_htmls['text'] = ''

for i in range(0, len(df_htmls)):
    print(i)
    print(df_htmls['link'][i])
    print('\n\n')
    try:
        df_htmls['dateline'][i] = get_dateline(df_htmls['link'][i])
    except:
        print('Failed to get dateline for ' + df_htmls['link'][i])
    try:
        df_htmls['text'][i] = get_text(df_htmls['link'][i])
    except:
        print('Failed to get text for ' + df_htmls['link'][i])
    print('Completed ' + str(i) + ' of ' + str(len(df_htmls)) + ' links')


## save html_links_data
df_htmls.to_csv('nonED/mmwr/data/files/p1B/html_links_data.csv', index=False)