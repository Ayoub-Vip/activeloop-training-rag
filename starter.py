from llama_index.core import download_loader
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor

Settings.embed_model = "text-embedding-ada-002"
Settings.llm_model = "gpt-3.5-turbo"

data_path = "./data"

loader = SimpleDirectoryReader(input_dir=data_path)
docs = loader.load_data()
vector_store = VectorStoreIndex.from_documents(documents=docs, show_progress=True,
                                               transformations=[])
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = storage_context.index_store

retriever = VectorIndexRetriever(index=index, similarity_top_k=5, )
response_synthesizer = get_response_synthesizer()

query_engine = RetrieverQueryEngine.from_args(
                    retriever=retriever,
                    response_synthesizer=response_synthesizer
                    node_postprocessors=[
                        SimilarityPostprocessor(similarity_cutoff=0.7)
                    ]
                )