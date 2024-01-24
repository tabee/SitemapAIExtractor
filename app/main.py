from sitemap_parser import SitemapParser

parser = SitemapParser('https://www.eak.admin.ch/eak/de/home.sitemap.xml')

try:
    filtered_urls = parser.get_urls(filter_str="/de/home/Firmen/")
    print(filtered_urls)
except Exception as e:
    print(f"An error occurred: {e}")