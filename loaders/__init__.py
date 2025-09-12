import os

from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from functools import partial

# from ..loaders.iterator import ResumableIterator
load_dotenv()

env = partial(os.getenv)
