class AIContentAnalyzer:
    """
    A class for analyzing web content with AI, using predefined prompts.

    Methods:
        analyze_content_prompt: Analyzes the content based on predefined prompts.
    """

    def __init__(self, prompts):
        """
        Initializes the AIContentAnalyzer with specific prompts.

        Args:
            prompts (list): A list of prompts.
        """
        self.prompts = {k: [word.lower() for word in v] for k, v in prompts.items()}

    def _analyze(self, text):
        """
        Analyzes the given text (content) with a predefined prompt.
        In theorie, the text can be html, denpending on the prompt.

        Args:
            text (str): The text to be analyzed.

        Returns:
            pipeline (Pipeline): a pipeline object
        """
        # implement pipeline here
        return None

    def analyze_content_prompt(self, content, prompts):
        """
        Analyzes the given content based on the prompt.

        Args:
            content (str): The content to be analyzed.
            prompt (str): The prompt to be used.

        Returns:
            list of str: A list of predefined, ai generated keywords, even if no keywords were found.
        """
        # run pipeline here with prompt
        return self._analyze(content)


# Beispielhafte Verwendung
if __name__ == "__main__":
    prompt_to_process = {
        "Verständlichkeit": ["Das ist ein LLM-Prompt"],
        "Genderwoke": ["Das ist ein LLM-Prompt"],
        # Weitere Prompts mit Regeln
    }
    analyzer = AIContentAnalyzer(prompt_to_process)

    content = "Dieser Produktionsplan informiert über die Termine im Zusammenhang mit der monatlichen Hauptzahlung der Familienausgleichskasse der Eidgenössischen Ausgleichskasse."

    print(analyzer.analyze_content_prompt(content))  # Gibt ['Firmen', 'Familienausgleichskasse'] zurück