import os
import chromadb

from typing import Annotated, Optional
from loguru import logger
from dotenv import load_dotenv
from pydantic import Field, PrivateAttr
from functools import partial
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import (StorageContext, ServiceContext, VectorStoreIndex)

from ..config import VECTOR_STORE_DIR, DATA_DIR, ParserParams


load_dotenv()

env = partial(os.getenv)

class ChromaVectorStoreBuilder:
    def __init__(self, db=None):
        self.db = db
        
    def connect_db(self, host=env('CHROMA_HOST'), port=env('CHROMA_PORT'), db_name=env('CHROMA_DB')):
        self.db = chromadb.HttpClient(
            host=host,
            port=port,
            database=db_name
        )

    def create_db(self, db_name=env('CHROMA_DB')):
        self.db = chromadb.PersistentClient(path=VECTOR_STORE_DIR / db_name)

    def create_collect(
        self,
        db: chromadb.ClientAPI=None,
        name: str = "quick_collection"
    ) -> chromadb.Collection:
        """create a collection given a chroma database, 

        Args:
            db (chromadb.ClientAPI, optional): a chroma client API to connect to. Defaults to None.
            name (str, optional): the name of the collection. Defaults to "quick_collection".

        Returns:
            chromadb.Collection: return the created collection object.
        """
        if db is None:
            self.db = connect_db()
        chroma_collection = db.get_or_create_collection(name=name)
        
        return chroma_collection

    def get_vector_store(
        self,
        db: chromadb.ClientAPI=None,
        collection: str="quick_collection"
    ) -> ChromaVectorStore:
        if db is None:
            self.db = connect_db()
        vector_store = ChromaVectorStore(db.get_collection(collection))
        
        return vector_store