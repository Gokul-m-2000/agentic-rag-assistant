from sqlalchemy.orm import Session

from db.models import Document,DocumentChunk


def create_document(
    session: Session,
    user_id: int,
    filename: str,
    file_type: str,
    storage_key: str,
    file_size: int,
) -> Document:
    document = Document(
        user_id=user_id,
        filename=filename,
        file_type=file_type,
        storage_key=storage_key,
        file_size=file_size,
        status="PROCESSING",
    )

    session.add(document)
    session.flush()

    return document


def create_document_chunk(
        session : Session,
        document_id : int,
        chunk_index: int,
        content: str,
        page_number: int | None,
        embedding: list[float],
        chunk_metadata: dict,
) ->DocumentChunk :
        chunk = DocumentChunk(
        document_id=document_id,
        chunk_index=chunk_index,
        content=content,
        page_number=page_number,
        embedding=embedding,
        chunk_metadata=chunk_metadata,
    )



        session.add(chunk)
        session.flush()

        return chunk
