from dotenv import load_dotenv
import os
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.pipeline_utils import build_rag_pipeline, build_indexing_pipeline
from haystack.pipeline_utils.indexing import download_files

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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
            prompt (str): The prompt to be used.
        """

        self.prompts = {k: [word for word in v] for k, v in prompts.items()}
        self.generation_model = "gpt-3.5-turbo-1106" # The latest GPT-3.5 Turbo model with a context window of 16385 tokens and improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.
        self.embedding_model = "intfloat/e5-base-v2"
        self.llm_api_key=OPENAI_API_KEY


    def _analyze(self, url):
        """
        Analyzes the given text (content) with a predefined prompt.
        In theorie, the text can be html, denpending on the prompt.

        Args:
            prompt (str): The prompt to be used.

        Returns:
            pipeline (Pipeline): a pipeline object
        """

        print(f"prompt: {self.prompts['Prompt1'][0]}")
        print(f"prompt: {self.prompts['Prompt2']}")
        # implement pipeline here

        document_store = InMemoryDocumentStore()
        files = download_files(sources=[url])

        # Indexing
        indexing_pipeline = build_indexing_pipeline(
            document_store=document_store,
            embedding_model=self.embedding_model,
            supported_mime_types=["text/plain", "text/html"],  # "application/pdf"
        )
        indexing_pipeline.run(files=files) 

        # RAG pipeline with vector-based retriever + LLM
        rag_pipeline = build_rag_pipeline(
            document_store=document_store,
            embedding_model=self.embedding_model,
            generation_model=self.generation_model,
            llm_api_key=self.llm_api_key,
        )

        # For details, like which documents were used to generate the answer, look into the result object
        result = rag_pipeline.run(query=self.prompts['Prompt1'][0])
        #print(result.data)








        return result.data

    def analyze_content_by_llm(self, url):
        """
        Analyzes the given content based on the pre-defined prompts.

        Args:
            content (str): The content to be analyzed.
        Returns:
            list of str: A list of predefined, ai generated keywords, even if no keywords were found.
        """
        # run pipeline here with prompt
        return self._analyze(url)


# Beispielhafte Verwendung
if __name__ == "__main__":
    prompts_to_process = {
        "Prompt1": ["Fasste die wichtigsten Punkte zusammen und erstelle einen SEO konformen Webseiten Titel. Beginne mit dem Wort 'Titel:' gefolgt von einem Emoij."],
        "Prompt2": ["Prüfe auf diskriminierende Inhalte, wie z.B. männliche Formulierungen."],
        # Weitere Prompts mit Regeln
    }
    analyzer = AIContentAnalyzer(prompts_to_process)

    url = "https://www.eak.admin.ch/eak/de/home/reform-ahv21/ueberblick/rentenzuschlag.html"

    print(analyzer.analyze_content_by_llm(url))  # was kommt hier raus?