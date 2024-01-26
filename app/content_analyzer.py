from bs4 import BeautifulSoup

class ContentAnalyzer:
    """
    A class for analyzing web content without AI, using predefined keywords and rules.

    Methods:
        analyze_content(content): Analyzes the content based on predefined rules or keywords.
        analyze_url(url): Analyzes the URL based on predefined rules or keywords.
    """

    def __init__(self, keywords_rules, default_keyword="Sonstiges"):
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
