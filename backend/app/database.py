"""Database connection and session management."""
import psycopg2
import logging
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class Database:
    """Database connection manager."""
    
    def __init__(self):
        self.connection_string = settings.database_url
    
    @contextmanager
    def get_connection(self):
        """Get a database connection with automatic cleanup."""
        logger.debug("Acquiring database connection")
        conn = psycopg2.connect(
            self.connection_string,
            cursor_factory=RealDictCursor
        )
        try:
            logger.debug("Database connection established")
            yield conn
            logger.debug("Committing transaction")
            conn.commit()
            logger.debug("Transaction committed successfully")
        except Exception as e:
            logger.error(f"Database error occurred: {str(e)}", exc_info=True)
            logger.warning("Rolling back transaction")
            conn.rollback()
            raise
        finally:
            conn.close()
            logger.debug("Database connection closed")
    
    @contextmanager
    def get_cursor(self, connection=None):
        """Get a database cursor with automatic cleanup.
        
        If connection is provided, use it (for transaction-based operations).
        Otherwise, create a new connection.
        """
        if connection:
            # Use provided connection (don't close it - caller manages lifecycle)
            logger.debug("Creating cursor from provided connection")
            cursor = connection.cursor()
            try:
                yield cursor
            finally:
                cursor.close()
                logger.debug("Cursor closed")
        else:
            # Create a new connection for single operations
            logger.debug("Creating new connection for single operation")
            with self.get_connection() as conn:
                cursor = conn.cursor()
                try:
                    yield cursor
                finally:
                    cursor.close()
                    logger.debug("Cursor closed")


# Global database instance
db = Database()

