""" A module to parse sitemaps and extract URLs. """
import xml.etree.ElementTree as ET
import requests

class SitemapParser:
    """
    A class to parse sitemaps and extract URLs.

    Attributes:
        sitemap_url (str): The URL of the sitemap to be parsed.

    Methods:
        get_urls(filter_str=None): Extracts and optionally filters URLs from the sitemap.
    """

    def __init__(self, sitemap_url):
        """
        Initializes the SitemapParser with a specified sitemap URL.

        Args:
            sitemap_url (str): The URL of the sitemap to parse.
        """
        self.sitemap_url = sitemap_url

    def get_urls(self, filter_str=None):
        """
        Retrieves URLs from the sitemap and applies an optional filter.

        This method fetches the sitemap from the specified URL, parses it,
        and extracts a list of URLs. If a filter string is provided, only URLs
        containing the filter string are returned.

        Args:
            filter_str (str, optional): A string to filter the URLs. 
                                        Defaults to None, which means no filter is applied.

        Returns:
            list of str: A list of URLs extracted from the sitemap. If a filter is applied,
                         only URLs containing the filter string are included.

        Raises:
            requests.RequestException: If there is an issue with network access.
            xml.etree.ElementTree.ParseError: If there is an error parsing the XML.
        """
        try:
            # Fetching the XML data
            response = requests.get(self.sitemap_url)
            response.raise_for_status()  # Raises an exception for HTTP errors
        except requests.RequestException as request_exception:
            raise requests.RequestException(f"Failed to retrieve sitemap: {request_exception}")

        try:
            # Parsing the XML data
            root = ET.fromstring(response.content)

            # Extracting URLs
            urls = [url.text for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

            # Applying the filter if provided
            if filter_str:
                urls = [url for url in urls if filter_str in url]

            return urls
        except ET.ParseError as parse_error:
            raise ET.ParseError(f"Failed to parse XML data: {parse_error}")

# Example usage
if __name__ == "__main__":
    SITEMAP_URL = 'https://www.eak.admin.ch/eak/de/home.sitemap.xml'
    parser = SitemapParser(SITEMAP_URL)

    try:
        filtered_urls = parser.get_urls(filter_str="/de/home/Firmen/Anschluss/")
        print(filtered_urls)
    except Exception as e:
        print(f"An error occurred: {e}")
