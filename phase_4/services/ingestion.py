

from services.embedding import get_embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from settings import settings
from exceptions import DocumentSplitError,DocumentEmbeddingError
from langchain_core.documents import Document
from db.repositories.documents import create_document,create_document_chunk
from sqlalchemy.orm import Session
import logging




logger = logging.getLogger(__name__)


def split_documents(documents : list[Document] ) -> list[Document]:

        try:
            if not documents:
                logger.error("No documents provided for splitting")
                raise DocumentSplitError("No documents provided for splitting")
            logger.info("Starting document splitting")
            splitter=RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.overlap
                )
            chunks=splitter.split_documents(documents)
            logger.info("Documents split into chunks: count=%d", len(chunks))
            if not chunks:
                logger.error("No chunks were produced")
                raise DocumentSplitError("no chunks available !")

            valid_chunks=[chunk for chunk in chunks if chunk.page_content.strip()]
            if not valid_chunks:
                logger.error("No valid chunks available")
                raise DocumentSplitError("No valid chunks were produced")
            logger.info("Valid chunks: count=%d", len(valid_chunks))

            return valid_chunks
        except DocumentSplitError:
            raise
        except Exception as e:
            logger.exception("An unexpected error while splitting documents")
            raise DocumentSplitError("Failed to split documents") from e



def embed_chunks(chunks:  list[Document]) -> list[list[float]]:
    try:
        if not chunks:
            logger.error("No chunks provided for embedding")
            raise DocumentEmbeddingError("No chunks provided for embedding")
        logger.info("Starting embedding of chunks")

        embeddings = get_embedding_model()

        vectors=embeddings.embed_documents([chunk.page_content for chunk in chunks])
        if len(vectors) != len(chunks):
            logger.error("Mismatch between number of chunks and embeddings")
            raise DocumentEmbeddingError("Mismatch between number of chunks and embeddings")
        logger.info("Chunks embedded successfully: count=%d", len(vectors))
        return vectors
    except DocumentEmbeddingError:
        raise
    except Exception as e:
        logger.exception("An unexpected error while embedding chunks")
        raise DocumentEmbeddingError("Failed to embed chunks") from e




def map_to_database(chunks: list[Document], vectors: list[list[float]]) -> list[dict]:

    if len(chunks) != len(vectors):
        logger.error("Mismatch between number of chunks and vectors")
        raise ValueError("Mismatch between number of chunks and vectors")

    mapped_data = []
    for index,(chunk,vector) in enumerate(zip(chunks,vectors)):
        mapped_data.append({
            "content":chunk.page_content,
            "metadata": chunk.metadata,
            "page_number":chunk.metadata.get("page"),
            "embedding":vector,
            "chunk_index":index


        })
    logger.info("Mapped data to database format successfully: count=%d", len(mapped_data))
    return mapped_data




def ingest_document(session : Session,
                    user_id: int,
                    filename: str,
                    file_type: str,
                    storage_key: str,
                    file_size: int,
                    documents: list[Document],
                  ) -> None :
    try:


        chunks=split_documents(documents)


        embedded_chunks=embed_chunks(chunks)

        mapped_chunks=map_to_database(chunks,embedded_chunks)

        document_obj=create_document(session,
                                user_id,
                                filename,
                                file_type,
                                storage_key,
                                file_size)

        for chunk in mapped_chunks:

            create_document_chunk(
                        session,
                        document_obj.id,
                        chunk['chunk_index'] ,
                        chunk['content'],
                        chunk['page_number'],
                        chunk['embedding'],
                        chunk['metadata'],
            )

        session.commit()


    except Exception:
        session.rollback()
        logger.exception("Document ingestion failed")
        raise