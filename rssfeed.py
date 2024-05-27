from datetime import datetime, timedelta
import feedparser
import ssl
from bs4 import BeautifulSoup
import pytz

ssl._create_default_https_context = ssl._create_unverified_context

# Define the UTC timezone
UTC = pytz.utc

# Define the UTC offset for 8 am
UTC_OFFSET = timedelta(hours=8)

# RSS feeds to fetch
DR_FEED = ['http://files.dre.pt/rss/serie1.xml',
           'https://files.dre.pt/rss/serie2&parte=a.xml',
           'https://files.dre.pt/rss/serie2&parte=c.xml']

SNS_FEED = 'https://www.sns.gov.pt/noticias/feed/'

DGS_FEED = ['https://rssproxy.migor.org/api/w2f?v=0.1&url=https%3A%2F%2Fwww.dgs.pt%2Fem-destaque.aspx&link=.%2Fh4%5B1%5D%2Fa%5B1%5D&context=%2F%2Fdiv%5B2%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B2%5D%2Fdiv%5B2%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv&re=none&out=atom']

INFARMED_FEED = ['https://www.infarmed.pt/web/infarmed/rss-agenda/-/asset_publisher/p30dUPCgMZh6/rss?p_p_cacheability=cacheLevelFull',
                 'https://www.infarmed.pt/web/infarmed/rss-alertas/-/asset_publisher/grlvtkM7UJK8/rss?p_p_cacheability=cacheLevelFull&_101_INSTANCE_grlvtkM7UJK8_currentURL=%2Fweb%2Finfarmed%2Frss-alertas&_101_INSTANCE_grlvtkM7UJK8_currentURL=%2Fweb%2Finfarmed%2Frss-alertas&_101_INSTANCE_grlvtkM7UJK8_currentURL=%2Fweb%2Finfarmed%2Frss-alertas&_101_INSTANCE_grlvtkM7UJK8_portletAjaxable=1&_101_INSTANCE_grlvtkM7UJK8_portletAjaxable=1&_101_INSTANCE_grlvtkM7UJK8_portletAjaxable=1',
                 'https://www.infarmed.pt/web/infarmed/rss-comunicados-de-imprensa/-/asset_publisher/19JAuDBUnYuY/rss?p_p_cacheability=cacheLevelFull&_101_INSTANCE_19JAuDBUnYuY_currentURL=%2Fweb%2Finfarmed%2Frss-comunicados-de-imprensa&_101_INSTANCE_19JAuDBUnYuY_currentURL=%2Fweb%2Finfarmed%2Frss-comunicados-de-imprensa&_101_INSTANCE_19JAuDBUnYuY_currentURL=%2Fweb%2Finfarmed%2Frss-comunicados-de-imprensa&_101_INSTANCE_19JAuDBUnYuY_portletAjaxable=1&_101_INSTANCE_19JAuDBUnYuY_portletAjaxable=1&_101_INSTANCE_19JAuDBUnYuY_portletAjaxable=1',
                 'https://www.infarmed.pt/web/infarmed/rss-noticias/-/asset_publisher/zQws9cSRmjar/rss?p_p_cacheability=cacheLevelFull&_101_INSTANCE_zQws9cSRmjar_currentURL=%2Fweb%2Finfarmed%2Frss-noticias&_101_INSTANCE_zQws9cSRmjar_currentURL=%2Fweb%2Finfarmed%2Frss-noticias&_101_INSTANCE_zQws9cSRmjar_currentURL=%2Fweb%2Finfarmed%2Frss-noticias&_101_INSTANCE_zQws9cSRmjar_portletAjaxable=1&_101_INSTANCE_zQws9cSRmjar_portletAjaxable=1&_101_INSTANCE_zQws9cSRmjar_portletAjaxable=1']

GOV_FEED = ['https://rssproxy.migor.org/api/w2f?v=0.1&url=https%3A%2F%2Fwww.portugal.gov.pt%2Fpt%2Fgc24%2Fcomunicacao%2Fintervencoes&link=.%2Fdiv%5B1%5D%2Fa%5B1%5D&context=%2F%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B4%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv&re=none&q=contains(%23any%2C%20%22Sa%C3%BAde%22)&out=atom',
            'https://rssproxy.migor.org/api/w2f?v=0.1&url=https%3A%2F%2Fwww.portugal.gov.pt%2Fpt%2Fgc24%2Fgoverno%2Fcomunicados-do-conselho-de-ministros&link=.%2Fdiv%5B1%5D%2Fa%5B1%5D&context=%2F%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B4%5D%2Fdiv%5B1%5D%2Fdiv%5B2%5D%2Fdiv&re=none&q=contains(%23any%2C%20%22sa%C3%BAde%22)&out=atom',
            'https://rssproxy.migor.org/api/w2f?v=0.1&url=https%3A%2F%2Fwww.portugal.gov.pt%2Fpt%2Fgc24%2Fcomunicacao%2Fnoticias&link=.%2Fdiv%5B1%5D%2Fa%5B1%5D&context=%2F%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv%5B4%5D%2Fdiv%5B1%5D%2Fdiv%5B1%5D%2Fdiv&re=none&q=contains(%23any%2C%20%22Sa%C3%BAde%22)&out=atom']

def fetch_new_items(rss_feed_urls):
    rss_items = []
    current_date = datetime.now(UTC).date()
    previous_date = current_date - timedelta(days=1)
    if current_date.weekday() == 0:  # Monday
           previous_date = current_date - timedelta(days=3)  # Friday

    # Calculate the datetime for 8 am UTC of the previous day
    previous_day_8am_utc = datetime.combine(previous_date, datetime.min.time()).replace(tzinfo=UTC) + UTC_OFFSET

    # Iterate over each RSS feed URL
    for rss_feed_url in rss_feed_urls:
        try:
            # Parse the RSS feed
            feed = feedparser.parse(rss_feed_url)
            # Iterate over the items in the feed
            for item in feed.entries:
                if "sns" in rss_feed_url or "infarmed" in rss_feed_url:
                    # Parse the publication date of the item
                    pub_date = datetime.strptime(item.published, "%Y-%m-%dT%H:%M:%S%z").astimezone(UTC).date()

                    # Check if the item is from the previous day after 8 am UTC
                    item_datetime = datetime.strptime(item.published, "%Y-%m-%dT%H:%M:%S%z").astimezone(UTC)
                    if pub_date >= previous_date and item_datetime >= previous_day_8am_utc:
                        # Extract relevant information from the item
                        title = item.title
                        link = item.link
                        # Add the item to the list of new items
                        rss_items.append({"title": title, "link": link, "pubDate": pub_date})
                elif "rssproxy" in rss_feed_url:
                    # Parse the publication date of the item
                    html_content = item.content[0].value
                    soup = BeautifulSoup(html_content, 'html.parser')
                    if rss_feed_url in GOV_FEED:
                        date_tag = soup.find('div', class_='dateItem')
                        date_str = date_tag.text.strip()
                        pub_date = datetime.strptime(date_str, '%Y-%m-%d às %Hh%M').astimezone(UTC).date()
                        item_datetime = datetime.strptime(date_str, '%Y-%m-%d às %Hh%M').astimezone(UTC)
                        if date_tag:
                            # Check if the item is from the previous day after 8 am UTC
                            if pub_date >= previous_date and item_datetime >= previous_day_8am_utc:
                                # Extract relevant information from the item
                                title = item.title
                                link = item.link
                                # Add the item to the list of new items
                                rss_items.append({"title": title, "link": link, "pubDate": pub_date})
                    elif rss_feed_url in DGS_FEED:
                        date_tag = soup.find('div', class_='register-date')
                        date_str = date_tag.text.strip()
                        pub_date = datetime.strptime(date_str, '%d-%m-%Y').date()
                        item_datetime = datetime.strptime(date_str, '%d-%m-%Y').replace(tzinfo=UTC)
                        if date_tag:
                            if pub_date >= previous_date:
                                # Extract relevant information from the item
                                title_tag = soup.find('h4', class_='register-title')
                                if title_tag:
                                    title = title_tag.get_text(strip=True)
                                else:
                                    title = item.title
                                link = item.link
                                # Add the item to the list of new items
                                rss_items.append({"title": title, "link": link, "pubDate": pub_date})
                    else:
                        break

                else:
                    # Extract relevant information from the item
                    if rss_feed_url in DR_FEED:
                        # For DR items, use the description as the title
                        description = item.description
                        title = BeautifulSoup(description, 'html.parser').text
                    else:
                        title = item.title
                    link = item.link
                    if "Saúde" in description or "saúde" in description:
                        # Add the item to the list of new items
                        rss_items.append({"title": title, "link": link})

        except Exception as e:
            print(f"An error occurred while fetching or parsing the feed '{rss_feed_url}': {e}")

    return rss_items

def main():
    gov_items = fetch_new_items(GOV_FEED)
    sns_items = fetch_new_items(SNS_FEED)
    dr_items = fetch_new_items(DR_FEED)
    infarmed_items = fetch_new_items(INFARMED_FEED)
    dgs_items = fetch_new_items(DGS_FEED)
    print(gov_items, sns_items, dr_items, infarmed_items, dgs_items)
    return dr_items, gov_items, sns_items, infarmed_items, dgs_items

if __name__ == "__main__":
    main()
