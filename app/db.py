# ===============================
# IMPORTS
# ===============================
from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID  # UUID column type for PostgreSQL; works with SQLite too
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID

# ===============================
# DATABASE CONFIGURATION
# ===============================
# DATABASE_URL defines how SQLAlchemy connects to the database.
# Here we are using SQLite with asynchronous access via aiosqlite.
# 'sqlite+aiosqlite:///./test.db' means:
#   - SQLite database engine
#   - Async driver: aiosqlite
#   - File path: ./test.db (relative path in current directory)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"


# ===============================
# BASE CLASS FOR ORM MODELS
# ===============================
# SQLAlchemy 2.0 requires that you create a subclass of DeclarativeBase for your models.
# Base.metadata will contain the schema information for all tables derived from this base.
class Base(DeclarativeBase):
    pass  # No additional logic needed; this serves as the declarative base class


class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")


# ===============================
# ORM MODEL DEFINITION
# ===============================
class Post(Base):  # Inherit from Base, not DeclarativeBase directly
    __tablename__ = "posts"  # Table name in the database

    # -------------------------------
    # COLUMN DEFINITIONS
    # -------------------------------

    # UUID primary key, auto-generated for each new record
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # Optional caption (TEXT column in database, can be NULL)
    caption = Column(Text)

    # File URL/path (STRING column, cannot be NULL)
    url = Column(String, nullable=False)

    # File type (STRING column, e.g., 'image/png'), required
    file_type = Column(String, nullable=False)

    # Original file name (STRING column), required
    file_name = Column(String, nullable=False)

    # Timestamp for creation
    # Uses a lambda to generate timezone-aware UTC datetime for every new row
    # Important: do NOT call datetime.now(timezone.utc) here directly,
    # because that would execute at import time rather than at row insertion.
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="posts")


# ===============================
# DATABASE ENGINE & SESSION SETUP
# ===============================

# Create an async engine.
# The engine manages the connection pool and sends SQL to the database.
# All queries will be executed asynchronously.
engine = create_async_engine(DATABASE_URL)

# Async session factory.
# Sessions are the interface for performing database operations: add, commit, query, delete.
# expire_on_commit=False keeps objects in memory after commit,
# which is often convenient for web apps.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# ===============================
# DATABASE INITIALIZATION FUNCTION
# ===============================
async def create_db_and_tables():
    """
    Creates all tables defined by ORM models that inherit from Base.
    Use this function at startup to ensure the database schema exists.

    async with engine.begin(): opens an async transaction
    conn.run_sync(): runs a synchronous SQLAlchemy call (create_all) in async context
    """
    async with engine.begin() as conn:  # Open an async connection and start a transaction
        await conn.run_sync(Base.metadata.create_all)  # Create all tables if they don't exist


# ===============================
# ASYNC SESSION PROVIDER
# ===============================
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an AsyncSession for use in async routes (like FastAPI dependency injection).

    How it works:
    - async_session_maker() creates a new session
    - 'async with' ensures the session is properly closed when done
    - 'yield session' allows the caller to use the session inside an async function
    """
    async with async_session_maker() as session:  # Open an async session
        yield session  # Provide session to caller
        # After the caller is done, the session automatically closes


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
     yield SQLAlchemyUserDatabase(session, User)
