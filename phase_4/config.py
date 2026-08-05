from pathlib import Path
from dotenv import load_dotenv


load_dotenv()



BASE_DIR=Path(__file__).resolve().parent
DATA_DIR=BASE_DIR/"data"
DOC_FILE=DATA_DIR/"doc.txt"
VECTOR_STORE_PATH=BASE_DIR/"vector_store"



EMBEDDING_MODEL = "gemini-embedding-001"
GENERATION_MODEL = "gemini-2.5-flash"
CHUNK_SIZE = 3000
OVERLAP = 1000
TOP_N_CHUNKS = 3
OUTPUT_DIMENSIONALITY = 3072