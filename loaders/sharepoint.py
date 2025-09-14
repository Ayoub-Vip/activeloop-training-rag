import os

from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from functools import partial

from llama_index.readers.microsoft_sharepoint import SharePointReader

load_dotenv()

env = partial(os.getenv)


loader = SharePointReader(
    client_id=env('SHAREPOINT_CLIENT_ID'),
    client_secret=env('SHAREPOINT_CLIENT_SECRET'),
    tenant_id=env('SHAREPOINT_TENANT_ID')
)
files_list = loader.list_resources()

documents = loader.load_data(
    # sharepoint_site_name=env(''),
    # sharepoint_folder_path=env(''),
    recursive=True,
)