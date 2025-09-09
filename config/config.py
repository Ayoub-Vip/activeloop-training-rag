from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm


# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
# RAW_DATA_DIR = DATA_DIR / "raw"
# INTERIM_DATA_DIR = DATA_DIR / "interim"
# PROCESSED_DATA_DIR = DATA_DIR / "processed"
# EXTERNAL_DATA_DIR = DATA_DIR / "external"

VECTOR_STORE_DIR = PROJ_ROOT / "vector_stores"

BOTS_DIR = PROJ_ROOT / "bots"
CHAINS_DIR = PROJ_ROOT / "chains"

# Custom
# ...


# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass