import requests
import pandas as pd
import bs4  # BeautifulSoup4

url = 'https://www.cdc.gov/mmwr/index2023.html'

# Get the HTML
response = requests.get(url)
response.raise_for_status()

# Parse the HTML
soup = bs4.BeautifulSoup(response.text, 'html.parser')

# Get the links that have volumes/72/ in them
links = soup.select('a[href*="volumes/72/"]')

# Create a separate links_html list that only keeps links with 72/wr/mm72 in them
links_html = [link for link in links if '72/wr/mm72' in link.attrs['href']]
len(links_html)


# Keep only the links that have a PDF
links = [link for link in links if link.attrs['href'].endswith('.pdf')]
links = ['https://www.cdc.gov' + link.attrs['href'] for link in links]

# Keep only the HTML links from links_html
links_html = ['https://www.cdc.gov' + link.attrs['href'] for link in links_html]

# Save the links to a CSV
df_pdfs = pd.DataFrame(links, columns=['link'])
df_htmls = pd.DataFrame(links_html, columns=['link'])

df_pdfs.to_csv('nonED/mmwr/data/files/p1A/pdf_links.csv', index=False)
df_htmls.to_csv('nonED/mmwr/data/files/p1A/html_links.csv', index=False)