from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import Document,DocumentChunk
import logging


logger=logging.getLogger(__name__)



def retrieve_chunks(session: Session,
                    user_id : int,
                    query_embedding : list[float],
                    top_k : int):


    try:

        if not query_embedding:
            logger.error("query embedding missing ")
            raise ValueError("Query embedding is missing")

        if top_k<=0:
            logger.error("Invalid top_k value :%d",top_k)
            raise ValueError("top_k must be greater than 0")

        distance= DocumentChunk.embedding.cosine_distance(query_embedding)

        statement=(
            select(
                DocumentChunk,
                distance.label("distance")
            )
            .join(Document,
                 DocumentChunk.document_id==Document.id
            )
            .where(Document.user_id==user_id)
            .order_by(distance)
            .limit(top_k)
        )

        results=session.execute(statement).all()

        return results

    except Exception:
        logger.exception("Chunk retrieval failed")
        raise