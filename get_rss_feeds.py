import feedparser

rss_url = "https://www.moneycontrol.com/rss/buzzingstocks.xml"
feed = feedparser.parse(rss_url)

if feed.entries:
    for entry in feed.entries:
        title = entry.get('title')
        link = entry.get('link')
        description = entry.get('description')
        published_date = entry.get('published')  # Or 'pubDate' depending on the feed
        guid = entry.get('guid')

        print("Title:", title)
        print("Link:", link)
        print("Description:", description)
        print("Published Date:", published_date)
        print("GUID:", guid)
        print("-" * 20)
else:
    print("No entries found in the RSS feed.")