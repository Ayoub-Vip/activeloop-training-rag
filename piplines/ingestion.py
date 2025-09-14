import os
import chromadb

from typing import Annotated, Optional
from loguru import logger
from dotenv import load_dotenv
from pydantic import Field, PrivateAttr

from llama_index.vector_stores.chroma import ChromaVectorStore

from ..config import VECTOR_STORE_DIR, DATA_DIR, ParserParams
from ..loaders import *

