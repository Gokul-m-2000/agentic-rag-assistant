"""
Shared configuration: loads environment variables and defines
constants used across the pipeline.
"""



import os
from dotenv import load_dotenv
from pathlib import Path



BASE_DIR=Path(__file__).resolve().parent

DATA_DIR=BASE_DIR/"data"

EVAL_DIR=BASE_DIR/"evaluation"



DOC_FILE=DATA_DIR/"doc.txt"

EMBEDDINGS_FILE=DATA_DIR/"embeddings.json"

GOLD_TEST_FILE=EVAL_DIR/"gold_test.json"

RUN_RESULTS_FILE=EVAL_DIR/"run_results.json"

EVAL_RESULTS_FILE=EVAL_DIR/"eval_results.json"

EVAL_LOG_FILE=EVAL_DIR/"eval_log.txt"


load_dotenv()



api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("api key is missing! ")


#gemini-3.1-flash-lite
EMBEDDING_MODEL = "gemini-embedding-001"
GENERATION_MODEL = "gemini-2.5-flash"
CHUNK_SIZE = 3000
OVERLAP = 1000
TOP_N_CHUNKS = 3
OUTPUT_DIMENSIONALITY = 3072