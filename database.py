import threading

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from settings import DATABASE_URL
from sqlalchemy.orm import sessionmaker, Session as SessionType


class DatabaseSingleton:
    """
    A singleton class to manage a single instance of the database engine and base.
    
    Attributes:
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine connected to the database.
        Base (sqlalchemy.ext.declarative.api.DeclarativeMeta): The base class for SQLAlchemy models.
        
    Methods:
        __new__(cls): Ensures that only one instance of DatabaseSingleton is created.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Creates or returns the singleton instance of the DatabaseSingleton class.
        
        This method ensures that the engine and base are only initialized once 
        and are thread-safe by using a lock to synchronize access to the singleton.
        
        Returns:
            DatabaseSingleton: The single instance of the class.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseSingleton, cls).__new__(cls)
                cls._instance.engine = create_engine(DATABASE_URL)
                cls._instance.Base = declarative_base()
        return cls._instance

    def create_session(cls) -> SessionType:
        """
        Creates and returns a new SQLAlchemy session using the engine from the singleton instance.

        Returns: 
            SessionType: A new SQLAlchemy session instance.
        """
        Session = sessionmaker(bind=cls._instance.engine)
        return Session()

db = DatabaseSingleton()
