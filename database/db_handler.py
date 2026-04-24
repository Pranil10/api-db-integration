import sqlite3
import logging


logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Handles SQLite database operations"""
    
    def __init__(self, db_path: str = "db/api_demo.db"):
        """
        Initialize database handler with connection path.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
    
    def connect(self):
        """Create a connection to the database"""
        return sqlite3.connect(self.db_path)
    
    def insert_post(self, user_id: int, post_id: int, title: str, body: str) -> bool:
        """
        Insert a post record into the database.
        
        Args:
            user_id: User ID from API
            post_id: Post ID from API
            title: Post title
            body: Post content
        
        Returns:
            bool: True if insertion was successful, False otherwise
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO posts (user_id, post_id, title, body) VALUES (?, ?, ?, ?)",
                (user_id, post_id, title, body)
            )
            
            conn.commit()
            conn.close()
            logger.info("Inserted post %s into database", post_id)
            return True
        
        except sqlite3.Error as e:
            logger.error("Database error during single insert: %s", e)
            return False
    
    def batch_insert_posts(self, posts_data: list) -> int:
        """
        Insert multiple post records into the database in a single batch operation.
        
        Args:
            posts_data: List of tuples (user_id, post_id, title, body)
        
        Returns:
            int: Number of posts successfully inserted
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.executemany(
                "INSERT INTO posts (user_id, post_id, title, body) VALUES (?, ?, ?, ?)",
                posts_data
            )
            
            conn.commit()
            inserted_count = cursor.rowcount
            conn.close()
            logger.info("Batch inserted %d posts into database", inserted_count)
            return inserted_count
        
        except sqlite3.Error as e:
            logger.error("Database error during batch insert: %s", e)
            return 0
    
    def get_all_posts(self) -> list:
        """
        Retrieve all posts from the database.
        
        Returns:
            list: List of tuples containing post data
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()
            conn.close()
            return posts
        except sqlite3.Error as e:
            logger.error("Database error while fetching posts: %s", e)
            return []
