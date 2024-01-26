import csv
from sitemap_parser import SitemapParser
from html_parser import HTMLParser
from content_analyzer import ContentAnalyzer

class ExtractedInformationAssembler:
    """
    A class to orchestrate the extraction of information from URLs in a sitemap, 
    analyze them using content and URL analyzers, and save the extracted data to a CSV file.

    Attributes:
        sitemap_url (str): URL of the sitemap to parse.
        rules_for_url (dict): Rules for URL keyword analysis.
        rules_for_content (dict): Rules for content keyword analysis.
        filter_str (str): String to filter URLs in the sitemap.
        content_class (str): CSS class name to identify the main content on a webpage.

    Methods:
        extract_information(): Extracts and stores information from filtered URLs.
        save_to_csv(filename): Saves the extracted information to a CSV file.
    """

    def __init__(self, sitemap_url, rules_for_url, rules_for_thema_by_url, rules_for_content, filter_urls_by, content_class):
        """
        Initializes the ExtractedInformationAssembler with all necessary components.

        Args:
            sitemap_url (str): URL of the sitemap to parse.
            rules_for_url (dict): Rules for URL keyword analysis.
            rules_for_content (dict): Rules for content keyword analysis.
            filter_str (str): String to filter URLs in the sitemap.
            content_class (str): CSS class name to identify the main content on a webpage.
        """
        self.sitemap_parser = SitemapParser(sitemap_url)
        self.html_parser = HTMLParser()
        self.url_analyzer = ContentAnalyzer(rules_for_url)
        self.url_analyzer_for_thema = ContentAnalyzer(rules_for_thema_by_url)
        self.content_analyzer = ContentAnalyzer(rules_for_content)
        # here will be the AIContentAnalyzer ...
        self.filter_str = filter_urls_by
        self.content_class = content_class
        self.extracted_data = []

    def extract_information(self):
        """
        Extracts information from the URLs in the sitemap that match the filter string.
        For each URL, extracts the page title, page lead, page content, and analyzes URL and content keywords.
        Stores the extracted information internally.
        """
        try:
            filtered_urls = self.sitemap_parser.get_urls(filter_str=self.filter_str)
            for url in filtered_urls:
                print(f"Extracting information from ...{url[-50:]}")
                page_title = self.html_parser.get_title(url)
                page_html_content = self.html_parser.get_html(url)
                page_content = self.html_parser.get_content_by_class(url, self.content_class)
                page_lead = self.html_parser.get_content_by_class_lead(url)
                page_last_modified_date = self.html_parser.get_last_modified_date_by_class_text_dimmed(url)
                url_keywords = self.url_analyzer.analyze_url(url)
                url_thema = self.url_analyzer_for_thema.analyze_url(url)
                page_content_keywords = self.content_analyzer.analyze_content(page_content)
                page_lead_keywords = self.content_analyzer.analyze_content(page_lead)
                page_have_iframe = self.content_analyzer.analyze_html_content_if_iframe(page_html_content)
                
                
                self.extracted_data.append({
                    "URL": url,
                    "Page Title": page_title,
                    "URL Keywords": url_keywords,
                    "URL Thema": url_thema,
                    "Content Keywords": page_content_keywords,
                    "Lead Keywords": page_lead_keywords,
                    "Page Leadtext": page_lead,
                    "Page Modified Date": page_last_modified_date,
                    "Have iframe": page_have_iframe,
                })
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_to_csv(self, filename):
        """
        Saves the extracted information to a CSV file.

        Args:
            filename (str): Name of the CSV file to save the data.
        """
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.extracted_data[0].keys())
            writer.writeheader()
            for data in self.extracted_data:
                writer.writerow(data)
