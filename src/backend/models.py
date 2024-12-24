from sqlalchemy import String, DateTime, ARRAY, Enum, UUID, Column, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base
import uuid
from datetime import datetime
import enum

class RankerType(enum.Enum):
    colpali = "colpali"
    bm25 = "bm25"
    hybrid = "hybrid"

class User(Base):
    __tablename__ = "app_user"

    user_id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    documents = relationship("UserDocument", back_populates="user")

class UserDocument(Base):
    __tablename__ = "user_document"

    document_id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("app_user.user_id"), nullable=False)
    document_name: Mapped[str] = mapped_column(String, nullable=False)
    file_extension: Mapped[str] = mapped_column(String, nullable=False)
    upload_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())

    user = relationship("User", back_populates="documents")

class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id = Column(UUID, ForeignKey("app_user.user_id"), primary_key=True)
    demo_questions = Column(ARRAY(String), default=list)
    ranker = Column(
        Enum(RankerType, name="ranker_type"),
        nullable=False,
        default=RankerType.colpali
    )
    gemini_token = Column(String, nullable=True)
    vespa_cloud_endpoint = Column(String, nullable=True)
    tenant_name = Column(String, nullable=True)
    app_name = Column(String, nullable=True)
    instance_name = Column(String, nullable=True)
    schema = Column(Text, nullable=True)
    prompt = Column(Text, nullable=True)

class ImageQuery(Base):
    __tablename__ = "image_queries"

    query_id = Column(String, primary_key=True)
    embeddings = Column(ARRAY(Float))
    text = Column(Text)
    is_visual_only = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
