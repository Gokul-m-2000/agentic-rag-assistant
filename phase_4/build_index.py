from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import logging
from logging_config import configure_logging
from settings import settings
from exceptions import SourceDocumentNotFoundError,IndexBuildError


logger=logging.getLogger(__name__)



def load_documents():
    try:
        if not settings.doc_file.exists():
                logger.warning("Source document not found: %s", settings.doc_file)
                raise SourceDocumentNotFoundError(f"Source document not found at {settings.doc_file}")
                    
        loader=TextLoader(settings.doc_file)
        documents=loader.load()
        logger.info("Documents loaded successfully: count=%d", len(documents))

        if not documents:
            logger.error("No documents found")
            raise ValueError("documents is empty")   

        return documents

    except SourceDocumentNotFoundError:
        raise
    except Exception as e:
        logger.exception(f"An unexpected error while loading documents")
        raise IndexBuildError("Failed to load documents") from e

def build_index(documents):

        try:
            logger.info("Starting index build process")
            splitter=RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.overlap
                )
            chunks=splitter.split_documents(documents)
            logger.info("Documents split into chunks: count=%d", len(chunks))
            if not chunks:
                logger.error("No chunks available")
                raise ValueError("no chunks available !")
            
            valid_chunks=[doc for doc in chunks if doc.page_content.strip()]
            if not valid_chunks:
                logger.error("No valid chunks found")
                raise ValueError("no valid chunks ! ")
            logger.info("Valid chunks: count=%d", len(valid_chunks))
            embeddings=GoogleGenerativeAIEmbeddings(
                                model=settings.embedding_model,
                                google_api_key=settings.google_api_key
                            )
                        
            db=FAISS.from_documents(valid_chunks,
                                        embeddings)
        
            
            db.save_local(settings.vector_store_path)
            logger.info("Vector store saved at %s", settings.vector_store_path)
            logger.info("index build successfully ")

            return db
       
        except Exception as e:
            logger.exception("An unexpected error while building index")
            raise IndexBuildError("Failed to build index") from e




if __name__=="__main__":
    configure_logging()
    documents=load_documents()
    db=build_index(documents)
    

            
