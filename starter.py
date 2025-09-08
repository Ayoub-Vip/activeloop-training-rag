import os

from pathlib import Path
from dotenv import load_dotenv
# from loguru import logger

from llama_index.core import download_loader
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser, SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core.vector_stores import FAISS
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
# from llma_index.cohere_reranker import CohereReranker
from llama_index.core.evaluation import generate_question_context_pairs

import wandb
load_dotenv()

Settings.embed_model = HuggingFaceInferenceAPIEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    token=os.getenv("HUGGINGFACES_TOKEN")
)
Settings.llm_model = OpenAI(model="gpt-3.5-turbo")

data_path = "./data"

loader = SimpleDirectoryReader(input_dir=data_path)
docs = loader.load_data()

# node_parser = SimpleNodeParser()
# nodes = node_parser.get_nodes_from_documents(documents=docs)

vector_store = FAISS()
storage_context = StorageContext.from_defaults(vector_store=vector_store)
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=48)
index = VectorStoreIndex.from_documents(documents=docs, show_progress=True,
                                               transformations=[
                                                   text_splitter
                                               ])

retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
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