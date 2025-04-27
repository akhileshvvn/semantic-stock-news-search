import feedparser
import json
import re
import string

rss_url = ["https://www.moneycontrol.com/rss/buzzingstocks.xml", #MoneyControl
           "https://www.investing.com/rss/news_25.rss", #Investing.com
           "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms", #Economic Times
           "http://rss.cnn.com/rss/money_markets.rss", #CNN
           "http://feeds.benzinga.com/benzinga", #Benzinga
           "https://www.thestreet.com/.rss/full/", #TheStreet
           "http://feeds.feedburner.com/zerohedge/feed", #ZeroHedge
           "https://polisen.se/aktuellt/rss/stockholms-lan/handelser-rss---stockholms-lan/", #Polisen
    ]

def clean_text(text):
    # Remove HTML tags, LOWERCASE, punctuation, and special characters
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    translator = str.maketrans('', '', string.punctuation)  # Create a translation table
    return text.translate(translator)  # Remove punctuation


df = []

for url in rss_url: 
    feed = feedparser.parse(url)
    if feed.entries:
        for entry in feed.entries:
            title = entry.get('title')
            link = entry.get('link')
            description = entry.get('description')
            published_date = entry.get('published')  # Or 'pubDate' depending on the feed
            guid = entry.get('guid')

            title = clean_text(title) if title else ''
            link = clean_text(link) if link else ''
            description = clean_text(description) if description else ''
            published_date = clean_text(published_date) if published_date else ''
            guid = clean_text(guid) if guid else ''

            df.append({
                'title': title,
                'link': link,
                'description': description,
                'published_date': published_date,
                'guid': guid
            })
    else:
        print("No entries found in the RSS feed.")
        print(url)

#print(df)

with open('mylist.json', 'w', encoding='utf-8') as file:
    json.dump(df, file, ensure_ascii=False, indent=4)