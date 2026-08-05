from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

from config import DOC_FILE,CHUNK_SIZE,OVERLAP,EMBEDDING_MODEL,VECTOR_STORE_PATH

load_dotenv()


def build_index():
    
        loader=TextLoader(DOC_FILE)
        documents=loader.load()
        if not documents:
            raise ValueError("documents is empty")

        splitter=RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=OVERLAP
            )
        chunks=splitter.split_documents(documents)
        if not chunks:
            raise ValueError("no chunks available !")
        
        valid_chunks=[doc for doc in chunks if doc.page_content.strip()]
        if not valid_chunks:
            raise ValueError("no valid chunks ! ")
        print(f"length of valid chunks {len(valid_chunks)}")
        embeddings=GoogleGenerativeAIEmbeddings(
                            model=EMBEDDING_MODEL
                        )
                    
        db=FAISS.from_documents(valid_chunks,
                                    embeddings)
        if db is None: 
            raise ValueError("db is None")
        
        db.save_local(VECTOR_STORE_PATH)
  
        

        return db


try:
        if __name__=="__main__":
            db=build_index()
            print("index build successfully ")
except FileNotFoundError:
        print("file not found")
except ValueError as e:
        print(e)

            
