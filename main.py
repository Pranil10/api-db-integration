import logging, os
from dotenv import load_dotenv
from api.api_client import get_json_data
from database.db_handler import DatabaseHandler
from db_initializer import initialize_database


logger = logging.getLogger(__name__)


def main():
    """Entry point for the app"""

    # Get environment variables
    load_dotenv()
    url = os.getenv("API_URL")
    db_name = os.getenv("DB_NAME")

    # Step 1: Initialize database
    logger.info("Step 1: Initializing database...")
    initialize_database(db_name)
    
    
    # Step 2: Fetch data from API
    logger.info("Step 2: Fetching data from API...")
    api_data = get_json_data(url)
    if not api_data:
        logger.error("Failed to fetch API data. Exiting.")
        return
    
    
    # Step 3: Parse and insert data into database
    logger.info("Step 3: Processing and inserting data...")
    db_handler = DatabaseHandler(db_name)
    
    if isinstance(api_data, list):
        # Prepare batch data
        batch_data = [
            (post.get("userId"), post.get("id"), post.get("title", ""), post.get("body", ""))
            for post in api_data
        ]
        # Batch insert all posts at once
        inserted = db_handler.batch_insert_posts(batch_data)
        if inserted == 0:
            logger.warning("No posts were inserted")
    else:
        logger.error("Unexpected API response format")
        return
    
    
    # Step 4: Display stored data
    logger.info("Step 4: Retrieving stored data...")
    posts = db_handler.get_all_posts()
    logger.info("Total posts stored: %d", len(posts))
    
    if posts:
        logger.info("Stored Posts:")
        logger.info("%s", "-" * 60)
        for post in posts[:5]:  # Display first 5 posts
            logger.info(f"Data - {post}")
            
    
    logger.info("%s", "=" * 60)
    logger.info("Demo completed successfully!")
    logger.info("%s", "=" * 60)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s : %(levelname)s : %(message)s")
    main()
