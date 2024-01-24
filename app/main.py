from sitemap_parser import SitemapParser
from html_parser import HTMLParser

# get a list of all URLs in the sitemap we want to crawl
parser = SitemapParser('https://www.eak.admin.ch/eak/de/home.sitemap.xml')

try:
    filtered_urls = parser.get_urls(filter_str="/eak/de/home/Firmen/familienzulagen/vorgehen/")
    print(f"\nWe found {len(filtered_urls)} URLs matching the filter.")
    #print(filtered_urls)
except Exception as e:
    print(f"An error occurred: {e}")


# extract information from each page
parser = HTMLParser()

for url in filtered_urls:
    print(f"\nExtracting information from page:\n{url}")
    try:
        page_title = parser.get_title(url)
        print(f"Page title:\n{page_title}")

        page_lead = parser.get_content_by_class(url, 'lead')
        print(f"Page lead:\n{page_lead}")

    except Exception as e:
        print(f"An error occurred: {e}")
