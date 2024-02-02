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
        self.document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")

        #self._index_documents(url)
        self.index_documents_from_website(url)

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


    def index_documents_from_website(self, url):
        """ 
        Indexes the given url in the document store.
        """
        from haystack import Pipeline
        from haystack.document_stores.in_memory import InMemoryDocumentStore
        from haystack.components.fetchers import LinkContentFetcher
        from haystack.components.converters import HTMLToDocument
        from haystack.components.preprocessors import DocumentCleaner
        from haystack.components.embedders import OpenAITextEmbedder, OpenAIDocumentEmbedder
        from haystack.components.writers import DocumentWriter
        
        print(f"Pre-Indexed {self.document_store.count_documents()} documents")

        fetcher = LinkContentFetcher()
        converter = HTMLToDocument()
        cleaner = DocumentCleaner()
        embedder = OpenAIDocumentEmbedder()
        writer = DocumentWriter(document_store = self.document_store)

        indexing_pipeline = Pipeline()
        indexing_pipeline.add_component(instance=fetcher, name="fetcher")
        indexing_pipeline.add_component(instance=converter, name="converter")
        indexing_pipeline.add_component(instance=cleaner, name="cleaner")
        indexing_pipeline.add_component(instance=embedder, name="embedder")
        indexing_pipeline.add_component(instance=writer, name="writer")

        indexing_pipeline.connect("fetcher.streams", "converter.sources")
        indexing_pipeline.connect("converter.documents", "cleaner.documents")
        indexing_pipeline.connect("cleaner.documents", "embedder.documents")
        indexing_pipeline.connect("embedder.documents", "writer.documents")
        

        indexing_pipeline.run(data={"fetcher": {"urls": [url]}})

        print(f"Post-Indexed {self.document_store.count_documents()} documents")



    def _processes_prompts(self, prompt_name):
        """
        Processes the given text (content) with a predefined prompt.
        In theorie, the text can be html, denpending on the prompt.

        Args:
            prompt (str): The prompt to be used.

        Returns:
            result data (str): a answer from the llm.
        """
        print(f"Post-Indexed {self.document_store.count_documents()} documents before RAG")
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


    def analyze_content_by_prompt(self, prompt_name):
        from haystack import Pipeline
        from haystack.document_stores.in_memory import InMemoryDocumentStore
        from haystack.components.embedders import OpenAITextEmbedder, OpenAIDocumentEmbedder
        from haystack.components.writers import DocumentWriter
        from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever

        query_pipeline = Pipeline()
        query_pipeline.add_component("text_embedder", OpenAITextEmbedder())
        query_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=self.document_store))
        query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

        query = self.prompts[prompt_name][0]
        # macht kein Sinn Dokumente zuerst suchen zu müssen!!!!
        result = query_pipeline.run({"text_embedder":{"text": query}})

        print(result['retriever']['documents'][0])

        # Document(id=..., mimetype: 'text/plain', 
        #  text: 'My name is Wolfgang and I live in Berlin')


    def processes_content_by_llm(self, prompt_name):
        """
        Processes the given content based on the pre-defined prompts.

        Args:
            prompt_name (str): The prompt to be used.
        Returns:
            llm anser (str): the answer from the llm depending on the prompt.
        """
        # run pipeline here with prompt
        return self.analyze_content_by_prompt(prompt_name)


# Beispielhafte Verwendung
if __name__ == "__main__":
    prompts_to_process = {
        "Prompt1": ["Erstelle einen SEO-konformen Website-Titel für folgenden Inhalt der Eidg. Ausgleichskasse EAK."],
        "Prompt2": ["Fasse ALLE wichtigen Aussagen im folgenden Text zusammen."],
        # Weitere Prompts
    }   
    # url = "https://www.eak.admin.ch/eak/de/home/reform-ahv21/ueberblick/ausgleichsmassnahmen.html"
    # analyzer = AIContentAnalyzer(prompts_to_process, url)
    # print(analyzer.processes_content_by_llm("Prompt1"))  # was kommt hier raus?    
    # print(analyzer.processes_content_by_llm("Prompt2"))  # was kommt hier raus?

    url = "https://www.eak.admin.ch/eak/de/home/EAK/publikationen/mitteilungs-archiv/eak-mitteilung-52.html"
    analyzer = AIContentAnalyzer(prompts_to_process, url)
    #print(analyzer.processes_content_by_llm("Prompt1"))  # was kommt hier raus?    
    print(analyzer.processes_content_by_llm("Prompt2"))  # was kommt hier raus?