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

    def __init__(self, sitemap_url, rules_for_url, rules_for_content, filter_str, content_class):
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
        self.content_analyzer = ContentAnalyzer(rules_for_content)
        self.filter_str = filter_str
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
                page_title = self.html_parser.get_title(url)
                page_content = self.html_parser.get_content_by_class(url, self.content_class)
                url_keywords = self.url_analyzer.analyze_url(url)
                content_keywords = self.content_analyzer.analyze_content(page_content)
                
                self.extracted_data.append({
                    "URL": url,
                    "Page Title": page_title,
                    "URL Keywords": url_keywords,
                    "Content Keywords": content_keywords
                })
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_to_csv(self, filename):
        """
        Saves the extracted information to a CSV file.

        Args:
            filename (str): Name of the CSV file to save the data.
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.extracted_data[0].keys())
            writer.writeheader()
            for data in self.extracted_data:
                writer.writerow(data)

# Beispielhafte Verwendung
if __name__ == "__main__":
    assembler = ExtractedInformationAssembler(
        sitemap_url='https://www.eak.admin.ch/eak/de/home.sitemap.xml',
        rules_for_url={
            "Firmen": ["firmen"], 
            "Private": ["dokumentation"],
            },
        rules_for_content={
            "AHV": ["alters- und hinterlassenenvorsorge", "ahv", "1. säule"], 
            "IV": ["Invalidenversicherung", " iv", "invalid"],
            "EO": ["erwerbsausfall", "eo", "erwerbsersatz", "mutterschaft", "vaterschaft"],
            "MSE": ["mutterschaftsentschädigung", "mse"],
            "FamZG": ["Familienzulagen", "famzg", "familienzulage", "familienzulagen"],
            "EAK": ["geschäftsleitung", "eak", "jahresbericht", "andrea steiner"],
            },
        filter_str="/eak/de/",
        content_class='main-content'
    )
    assembler.extract_information()
    assembler.save_to_csv('extracted_data.csv')
    print("Data extraction and CSV file creation completed.")
