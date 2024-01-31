import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

class ContentAnalyzer:
    """
    A class for analyzing web content without AI, using predefined keywords and rules.

    Methods:
        analyze_content(content): Analyzes the content based on predefined rules or keywords.
        analyze_url(url): Analyzes the URL based on predefined rules or keywords.
    """

    def __init__(self, keywords_rules=None, default_keyword="Sonstiges"):
        """
        Initializes the ContentAnalyzer with specific keywords and rules.

        Args:
            keywords_rules (dict): A dictionary mapping keywords to their respective rules.
            default_keyword (str): Default keyword to return if no rules match.
        """
        self.keywords_rules = {k: [word.lower() for word in v] for k, v in keywords_rules.items()}
        self.default_keyword = default_keyword

    def _analyze(self, text):
        """
        Analyzes the given text (content or URL) based on predefined keywords and rules.

        Args:
            text (str): The text to be analyzed.

        Returns:
            list of str: A list of matched predefined keywords, otherwise a list with default_keyword.
        """
        text = text.lower()
        matched_keywords = [keyword for keyword, contain_words in self.keywords_rules.items() if any(word in text for word in contain_words)]

        return matched_keywords if matched_keywords else [self.default_keyword]

    def analyze_content(self, content):
        """
        Analyzes the given content based on predefined keywords and rules.

        Args:
            content (str): The content to be analyzed.

        Returns:
            list of str: A list of matched predefined keywords, otherwise a list with default_keyword.
        """
        return self._analyze(content)

    def analyze_url(self, url):
        """
        Analyzes the given URL based on predefined keywords and rules.

        Args:
            url (str): The URL to be analyzed.

        Returns:
            list of str: A list of matched predefined keywords, otherwise a list with default_keyword.
        """
        return self._analyze(url)

    def analyze_url_depth(self, url):
        """
        Analyzes the given URL based on '/' and returns the depth of the URL.
        The homepage has a depth of 0.

        Args:
            url (str): The URL to be analyzed.

        Returns:
            count (int): A list of matched predefined keywords, otherwise a list with default_keyword.
        """
        return (len(url.split("/")) - 6)

    def analyze_html_content_if_image(self, html_content, excluded_image_urls=[
        '/eak/de/_jcr_content/copyright/image.imagespooler.png/1706709606228/logo.png',
        '/eak/de/_jcr_content/logo/image.imagespooler.png/1674124800670/logo.png', 
        '/eak/de/_jcr_content/navigation/icon.imagespooler.png/1674552485960/swiss.png', 
        ]):
        """
        Extracts all image URLs from the given html_content, excluding certain URLs.
        # @TODO: Add URL's and domain to the toml file!

        Args:
            html_content (str): The HTML content to be analyzed.
            excluded_urls (list): A list of URLs to be excluded.

        Returns:
            list: A list of image URLs found in the HTML content, excluding the specified URLs.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all("img")
        img_urls = ['https://www.eak.admin.ch'+img['src'] for img in img_tags if 'src' in img.attrs and img['src'] not in excluded_image_urls]
        if len(img_urls) == 0:
            return None
        return img_urls

    def analyze_list_of_image_urls(self, list_of_image_urls):
        """
        Returns true if at least one image has a width less than 1920 pixels, otherwise false.
        If no image is found, returns false.

        Args:
            list_of_image_urls (list): A list of URLs of images to be analyzed.

        Returns:
            bool: True if at least one image is less than 1920 pixels wide, otherwise False.
        """
        if list_of_image_urls == None:
                return False
        
        for url in list_of_image_urls:
            
            try:
                response = requests.get(url)
                response.raise_for_status()  # Sicherstellen, dass die Anfrage erfolgreich war

                image = Image.open(BytesIO(response.content))
                if image.size[0] < 1920:  # image.size[0] gibt die Breite des Bildes an
                    return True
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten beim Verarbeiten der URL {url}: {e}")
                continue  # Fortsetzung mit der nächsten URL, falls ein Fehler auftritt

        return False

    def analyze_html_content_if_iframe(self, html_content):
        """
        Analyzes the given html_content to see if in it is an iframe.

        Args:
            content (str): The html_content to be analyzed.

        Returns:
            bool: True if the soup object is an iframe, otherwise False.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.find("iframe") is not None

    def analyze_html_content_if_video(self, html_content):
        """
        Analyzes the given html_content to see if in it is a video.
        First, it checks if the html_content contains an iframe.
        If it does, it checks if the iframe contains a url with the word "vimeo" or "youtube" in it.

        Args:
            content (str): The html_content to be analyzed.

        Returns:
            bool: True if the soup object is a video, otherwise False.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        iframe = soup.find("iframe")
        if iframe is not None:
            url = iframe['src']
            return "vimeo" in url or "youtube" in url
        return False


    def analyze_count_of_words(self, content):
        """
        Analyzes the given content to see how many words it has.

        Args:
            content (str): The content to be analyzed.

        Returns:
            count (int): The number of words in the content.
        """
        return len(content.split())

# Beispielhafte Verwendung
if __name__ == "__main__":
    rules = {
        "Firmen": ["firmen", "connect", "Produktionsplan"],
        "Familienausgleichskasse": ["familienausgleichskasse", "ihr arbeitgeber"],
        # Weitere Schlüsselwörter und Regeln
    }
    analyzer = ContentAnalyzer(rules)

    content = "Dieser Produktionsplan informiert über die Termine im Zusammenhang mit der monatlichen Hauptzahlung der Familienausgleichskasse der Eidgenössischen Ausgleichskasse."
    url = "https://www.eak.admin.ch/eak/de/home/Firmen/familienzulagen/vorgehen/produktionsplan-2024.html"

    print(analyzer.analyze_content(content))  # Gibt ['Firmen', 'Familienausgleichskasse'] zurück
    print(analyzer.analyze_url(url))          # Gibt ['Firmen'] zurück
    print(analyzer.analyze_html_content_if_iframe(content))  # Gibt False zurück
    print(analyzer.analyze_url_depth(url))  # Gibt 4 zurück
    print(analyzer.analyze_count_of_words(content))  # Gibt 17 zurück
