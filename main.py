"""
    The main of the program
    use for set the URL, get the data from the scrapy, and load data to the database
"""

import os
from dotenv import load_dotenv
from etl.extract import extract_books
from etl.load import load_data


# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # URL to connect to the database
    URL = "https://books.toscrape.com/catalogue/category/books_1/page-1.html"

    # Get the scrapy data
    all_query = extract_books(URL)

    # Connet to the database and insert data
    mongo_uri = os.getenv("MONGO_URI")
    database_name = os.getenv("DATABASE")
    collection_name = os.getenv("COLLECTION")
    load_data(mongo_uri, database_name, collection_name, all_query)
