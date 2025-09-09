import os

from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
import chromadb
import wandb

from llama_index.core import download_loader
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser, SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import ServiceContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
# from llma_index.cohere_reranker import CohereReranker
from llama_index.core.evaluation import generate_question_context_pairs

from config import VECTOR_STORE_DIR, DATA_DIR, ParserParams


load_dotenv()

Settings.embed_model = HuggingFaceInferenceAPIEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    token=os.getenv("HUGGINGFACE_TOKEN")
)
Settings.llm_model = OpenAI(model="gpt-3.5-turbo")
Settings.chunk_size = ParserParams.chunks_size
Settings.chunk_overlap = ParserParams.chunks_ovelap

loader = SimpleDirectoryReader(input_dir=DATA_DIR)
docs = loader.load_data()

# node_parser = SimpleNodeParser()  # this can be simply ingested in vector store in transformers
# nodes = node_parser.get_nodes_from_documents(documents=docs)

db = chromadb.PersistentClient(path=VECTOR_STORE_DIR / "chroma_db")
# chroma_client = chromadb.EphemeralClient()
chroma_collection = db.get_or_create_collection(name="quick_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
service_context = ServiceContext() #llm and embed_moel globally set 
storage_context = StorageContext.from_defaults(vector_store=vector_store)
text_splitter = SentenceSplitter()
index = VectorStoreIndex(nodes=docs, service_context=service_context,
                         storage_context=storage_context,
                         transformations=[
                                            text_splitter
                            ],
                         show_progress=True)

retriever = VectorIndexRetriever(index=index, similarity_top_k=15)
response_synthesizer = get_response_synthesizer()
query_engine = RetrieverQueryEngine.from_args(
                    retriever=retriever,
                    response_synthesizer=response_synthesizer,
                    node_postprocessors=[
                        SimilarityPostprocessor(similarity_cutoff=0.7)
                    ]
                )

######################## Evaluation ########################
context_questions = generate_question_context_pairs(docs)
print(context_questions.model_dump_json())