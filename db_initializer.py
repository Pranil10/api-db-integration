import sqlite3
import os
import logging


logger = logging.getLogger(__name__)


def initialize_database(db_path: str = "db/api_demo.db"):
    """
    Create SQLite database and initialize tables.
    
    Args:
        db_path: Path to the SQLite database file
    """
    # Create db directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL UNIQUE,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully at %s", db_path)
        return True
    
    except sqlite3.Error as e:
        logger.error("Error initializing database: %s", e)
        return False


if __name__ == "__main__":
    initialize_database()
