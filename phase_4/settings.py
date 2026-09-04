from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict


BASE_DIR=Path(__file__).resolve().parent


class Settings(BaseSettings):
    google_api_key:str 
    embedding_model:str="gemini-embedding-001"
    generation_model:str="gemini-2.5-flash"
    chunk_size:int=3000
    overlap:int=1000
    top_n_chunks: int = 3
    output_dimensionality: int = 3072

    model_config=SettingsConfigDict(env_file=BASE_DIR.parent / ".env")

    @property
    def data_dir(self):
        return BASE_DIR/"data"
        
    @property
    def doc_file(self):
        return self.data_dir/"doc.txt"

    @property
    def vector_store_path(self):
        return BASE_DIR/"vector_store"




settings=Settings()   


# print(settings)
# print(settings.chunk_size)
# print(settings.overlap)
# print(settings.data_dir)
# print(settings.doc_file)
# print(settings.vector_store_path)