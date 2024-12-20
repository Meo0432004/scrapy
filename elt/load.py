"""
    Use for connect to the database and execute insert query
"""

from config import log
from config.database import DatabaseConfig


def load_data(mongo_uri, database_name, collection_name, data: list):
    """
    Insert data into MongoDB collection.

    :param data: List of documents to insert
    """

    if not mongo_uri or not database_name or not collection_name:
        log.log_error("Missing MongoDB connection settings.")
        return None

    collection = DatabaseConfig.connect_to_database(
        mongo_uri, database_name, collection_name
    )
    if collection is not None:
        try:
            collection.insert_many(data)
            log.log_message(f"Inserted {len(data)} records successfully.")
        except Exception as e:
            log.log_error("Error inserting data into MongoDB.", e)
