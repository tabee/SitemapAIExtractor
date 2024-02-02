from dotenv import load_dotenv
import os
from haystack import Pipeline
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.preprocessors import DocumentCleaner
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
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
        self.url = url



    def index_and_answer_documents_from_website(self, prompt_name):
        """ 
        Indexes the given url in the document store.
        """
        fetcher = LinkContentFetcher()
        converter = HTMLToDocument()
        cleaner = DocumentCleaner()

        prompt_template = """
            Given these documents, answer the question.\nDocuments:
            {% for doc in documents %}
            {{ doc.content }}
            {% endfor %}

            \nQuestion: {{query}}
            \nAnswer:
            """

        p = Pipeline()
        p.add_component(instance=fetcher, name="fetcher")
        p.add_component(instance=converter, name="converter")
        p.add_component(instance=cleaner, name="cleaner")

        p.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
        p.add_component(instance=OpenAIGenerator(api_key=os.environ.get("OPENAI_API_KEY")), name="llm")
        p.add_component(instance=AnswerBuilder(), name="answer_builder")

        p.connect("fetcher.streams", "converter.sources")
        p.connect("converter.documents", "cleaner.documents")
        p.connect("cleaner.documents", "prompt_builder")
        p.connect("prompt_builder", "llm")
        p.connect("llm.replies", "answer_builder.replies")
        
        query = self.prompts[prompt_name][0]

        result = p.run(
            {
                "fetcher": {"urls": [self.url]},
                "prompt_builder": {"query": query},
                "answer_builder": {"query": query},
            })
        print(result['answer_builder']['answers'])





# Beispielhafte Verwendung
if __name__ == "__main__":
    prompts_to_process = {
        "Prompt1": ["Erstelle einen SEO-konformen Website-Titel für folgenden Inhalt der Eidg. Ausgleichskasse EAK."],
        "Prompt2": ["Fasse ALLE wichtigen Aussagen im folgenden Text zusammen."],
        # Weitere Prompts
    }
    url = "https://www.eak.admin.ch/eak/de/home/EAK/publikationen/mitteilungs-archiv/eak-mitteilung-52.html"
    analyzer = AIContentAnalyzer(prompts_to_process, url)
    print(analyzer.index_and_answer_documents_from_website(prompt_name="Prompt1"))  # was kommt hier raus?    
    print(analyzer.index_and_answer_documents_from_website(prompt_name="Prompt2"))  # was kommt hier raus?