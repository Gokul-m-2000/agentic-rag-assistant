from datetime import datetime,timezone
from sqlalchemy import DateTime,String,ForeignKey,Text
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector



class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column (primary_key  =True)
    api_key_hash: Mapped[str] = mapped_column (String(255),nullable = False)
    created_at: Mapped[datetime] = mapped_column   (
        DateTime (timezone = True),
        default = lambda : datetime.now (timezone.utc),
        nullable = False,)
    updated_at: Mapped[datetime] = mapped_column (
        DateTime (timezone = True),
        default = lambda : datetime.now (timezone.utc),
        onupdate = lambda : datetime.now (timezone.utc),
        nullable = False,)



class Document(Base):
    __tablename__="documents"
    id: Mapped[int] = mapped_column (primary_key  =True)
    user_id: Mapped[int] = mapped_column (ForeignKey("users.id"),  nullable = False)
    filename: Mapped[str] = mapped_column (String(255),nullable = False)
    file_type: Mapped[str] = mapped_column (String(50),nullable = False)
    storage_key: Mapped[str] = mapped_column (String(255),nullable = False)
    file_size: Mapped[int] = mapped_column (nullable = False)
    status: Mapped[str] = mapped_column (String(50),nullable = False,default="PROCESSING")
    created_at: Mapped[datetime] = mapped_column   (
        DateTime (timezone = True),
        default = lambda : datetime.now (timezone.utc),
        nullable = False,)
    updated_at: Mapped[datetime] = mapped_column (
        DateTime (timezone = True),
        default = lambda : datetime.now (timezone.utc),
        onupdate = lambda : datetime.now (timezone.utc),
        nullable = False,)



class DocumentChunk(Base):
    __tablename__="document_chunks"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    document_id : Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    page_number: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(3072),
        nullable=False,
    )

    chunk_metadata: Mapped[dict] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )