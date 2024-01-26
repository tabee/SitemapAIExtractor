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

    def __init__(self, prompts, url):
        """
        Initializes the AIContentAnalyzer with specific prompts and one url.

        Args:
            prompt (str): The prompt to be used.
            url (str): The url to be analyzed.
        """

        self.prompts = {k: [word for word in v] for k, v in prompts.items()}
        self.generation_model = "gpt-3.5-turbo-1106" # The latest GPT-3.5 Turbo model with a context window of 16385 tokens and improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens.
        self.embedding_model = "intfloat/e5-base-v2"
        self.llm_api_key=OPENAI_API_KEY
        self.document_store = InMemoryDocumentStore()

        self._index_documents(url)

    def _index_documents(self, url):
        """ 
        Indexes the given url in the document store.
        @TODO: This should be done in the background, not in the constructor.
        @TODO: we really should not index the page in many documents.
        
        Args:
            url (str): The url to be indexed.
        """
        files = download_files(sources=[url])
        indexing_pipeline = build_indexing_pipeline(
            document_store=self.document_store,
            embedding_model=self.embedding_model,
            supported_mime_types=["text/plain", "text/html", "application/pdf"],
        )
        indexing_pipeline.run(files=files)

    def _processes_prompts(self, prompt_name):
        """
        Processes the given text (content) with a predefined prompt.
        In theorie, the text can be html, denpending on the prompt.

        Args:
            prompt (str): The prompt to be used.

        Returns:
            result data (str): a answer from the llm.
        """
        
        # RAG pipeline with vector-based retriever + LLM
        rag_pipeline = build_rag_pipeline(
            document_store=self.document_store,
            embedding_model=self.embedding_model,
            generation_model=self.generation_model,
            llm_api_key=self.llm_api_key,
        )
        result = rag_pipeline.run(query=self.prompts[prompt_name][0])
        #print(f"Indexed {self.document_store.count_documents()} documents")
        return result.data

    def processes_content_by_llm(self, prompt_name):
        """
        Processes the given content based on the pre-defined prompts.

        Args:
            prompt_name (str): The prompt to be used.
        Returns:
            llm anser (str): the answer from the llm depending on the prompt.
        """
        # run pipeline here with prompt
        return self._processes_prompts(prompt_name)


# Beispielhafte Verwendung
if __name__ == "__main__":
    prompts_to_process = {
        "Prompt1": ["Erstelle einen SEO-konformen Website-Titel für folgenden Inhalt der Eidg. Ausgleichskasse EAK."],
        "Prompt2": ["Prüfe den Text auf diskriminierende Inhalte. Wenn du sie findest, zitiere den entsprechenden Sart und begünde. ansonsten gib unbedingt nur 'ok' ohne Begründung zurück."],
        # Weitere Prompts
    }   
    url = "https://www.eak.admin.ch/eak/de/home/EAK/portrait.html"
    analyzer = AIContentAnalyzer(prompts_to_process, url)
    print(analyzer.processes_content_by_llm("Prompt1"))  # was kommt hier raus?    
    print(analyzer.processes_content_by_llm("Prompt2"))  # was kommt hier raus?