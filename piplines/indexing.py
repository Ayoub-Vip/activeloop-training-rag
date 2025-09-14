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
    """this class is useful to create/connect/manage a Chroma vector store.
    """
    def __init__(self, db=None):
        self.db = db
        
    def connect_db(
        self,
        host=env('CHROMA_HOST'),
        port=env('CHROMA_PORT'),
        db_name=env('CHROMA_DB')
        ) -> None:
        self.db = chromadb.HttpClient(
            host=host,
            port=port,
            database=db_name
        )

    def create_db(self, db_name: str=env('CHROMA_DB')) -> None:
        """create a chroma database in VECTOR_STORE_DIR path / db_name

        Args:
            db_name (str, optional): the name of the chroma database. Defaults to env('CHROMA_DB').
        """
        self.db = chromadb.PersistentClient(path=VECTOR_STORE_DIR / db_name)

    def create_collect(
        self,
        name: str = "quick_collection"
    ) -> chromadb.Collection:
        """create a collection given a chroma database, 

        Args:
            name (str, optional): the name of the collection. Defaults to "quick_collection".

        Returns:
            chromadb.Collection: return the created collection object.
        """
        if self.db is None:
            self.db = self.connect_db()
        chroma_collection = self.db.get_or_create_collection(name=name)
        
        return chroma_collection

    def get_vector_store(
        self,
        collection: str="quick_collection"
    ) -> ChromaVectorStore:
        if self.db is None:
            self.db = self.connect_db()
        vector_store = ChromaVectorStore(self.db.get_collection(collection))
        
        return vector_store