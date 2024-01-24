import requests
from bs4 import BeautifulSoup

class HTMLParser:
    """
    A class to parse HTML content from a given URL.

    Methods:
        get_html(url): Retrieves the raw HTML content of the specified URL.
        get_title(url): Extracts the title of the web page from the specified URL.
        get_content_by_class(url, css_class): Extracts content from all elements with the specified CSS class.
    """

    def get_html(self, url):
        """
        Fetches the raw HTML content from a specified URL.

        Args:
            url (str): The URL from which to fetch the HTML content.

        Returns:
            str: The raw HTML content.

        Raises:
            requests.RequestException: If there is an issue with network access or HTTP error.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to retrieve HTML content: {e}")

    def get_title(self, url):
        """
        Extracts the title of a web page from its HTML content.

        Args:
            url (str): The URL of the web page to extract the title from.

        Returns:
            str: The title of the web page.

        Raises:
            requests.RequestException: If there is an issue with network access or HTTP error.
        """
        try:
            html_content = self.get_html(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.title.string if soup.title else 'No title found'
            return title
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to retrieve page title: {e}")

    def get_content_by_class(self, url, css_class):
        """
        Fetches and concatenates the text content of all elements with a specified CSS class.

        Args:
            url (str): The URL from which to fetch the content.
            css_class (str): The CSS class to filter the content.

        Returns:
            str: Concatenated text content of all elements with the specified CSS class.

        Raises:
            requests.RequestException: If there is an issue with network access or HTTP error.
        """
        try:
            html_content = self.get_html(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.find_all(class_=css_class)
            return ' '.join(element.get_text() for element in elements)
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to retrieve content for class {css_class}: {e}")


# Example usage
if __name__ == "__main__":
    TEST_URL = 'https://www.eak.admin.ch/eak/de/home/Firmen/Anschluss.html'
    parser = HTMLParser()

    try:
        # html_content = parser.get_html(TEST_URL)
        # print(f"HTML content:\n{html_content}\n\n")

        page_title = parser.get_title(TEST_URL)
        print(f"Page title:\n{page_title}\n\n")

        page_lead = parser.get_content_by_class(TEST_URL, 'lead')
        print(f"Page lead:\n{page_lead}\n\n")

        page_maincontent = parser.get_content_by_class(TEST_URL, 'main-content')
        print(f"Page main-content:\n{page_maincontent}\n\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")
