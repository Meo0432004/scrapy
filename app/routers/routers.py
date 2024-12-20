"""
This module contains the FastAPI router definitions for managing books in the MongoDB database.

It includes endpoints for:
- Retrieving all books
- Retrieving a book by ID
- Creating a new book
- Updating an existing book
- Deleting a book by ID
"""

import os
from fastapi import APIRouter
from fastapi import HTTPException
from dotenv import load_dotenv
from bson import ObjectId
from app.convert.convert import book_scrap, books_scrap
from config.database import DatabaseConfig
from model.schema import BookScrap


# Load environment variables
load_dotenv()


endPoints = APIRouter()

mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DATABASE")
collection_name = os.getenv("COLLECTION")
book_db = book_db = DatabaseConfig.connect_to_database(
    mongo_uri, database_name, collection_name
)


@endPoints.get("/")
def home():
    """
    Health check endpoint to verify the FastAPI service is running.
    """
    return {"status": "Ok", "message": "My fast API is running"}


@endPoints.get("/all/books")
def get_all_books():
    """
    Retrieve all books from the MongoDB collection.

    :return: JSON response containing the list of all books.
    """
    books_data = book_db.find()
    converted_books = books_scrap(books_data)
    return {"status": "Ok", "data": converted_books}


@endPoints.get("/get/book/{book_id}")
def get_book(book_id: str):
    """
    Retrieve a single book by its ObjectId.

    :param book_id: The ID of the book to retrieve.
    :return: JSON response with the book details.
    """
    try:
        query = {"_id": ObjectId(book_id)}  # Convert id to ObjectId
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ObjectId: {e}") from e

    book_data = book_db.find_one(query)

    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")

    converted_book = book_scrap(book_data)
    return {"status": "Ok", "data": converted_book}


@endPoints.post("/create/book")
def create_book(book_data: BookScrap):
    """
    Create a new book in the MongoDB collection.

    :param book_data: The book data in the form of a Pydantic model.
    :return: JSON response with the ID of the newly created book.
    """
    book_dict = book_data.model_dump()
    result = book_db.insert_one(book_dict)

    return {"status": "201", "data": str(result.inserted_id)}


@endPoints.delete("/delete/{book_id}")
def delete_book(book_id: str):
    """
    Delete a book from the MongoDB collection by its ObjectId.

    :param book_id: The ID of the book to delete.
    :return: JSON response indicating the deletion status.
    """
    try:
        query = {"_id": ObjectId(book_id)}
        conversation_delete = book_db.find_one(query)
        if conversation_delete is not None:
            result = book_db.delete_one(query)
            return {
                "status": "Ok",
                "message": "the book is deleted",
                "data": result.deleted_count,
            }
        else:
            raise HTTPException(status_code=404, detail="The book is not found")
    except HTTPException as e:
        return {"status": "Error", "message": f"An error occurred: {e}"}


@endPoints.patch("/update/{book_id}")
def update_book(book_id: str, book_data: BookScrap):
    """
    Update an existing book in the MongoDB collection.

    :param book_id: The ID of the book to update.
    :param book_data: The updated book data in the form of a Pydantic model.
    :return: JSON response indicating the update status.
    """
    query = {"_id": ObjectId(book_id)}

    # Convert the Pydantic model to a dictionary
    book_dict = book_data.model_dump()  # This will convert the Pydantic model to a dict

    # Check if BookDetails is a Pydantic model or already a dictionary
    if isinstance(book_dict["BookDetails"], dict):
        # If it's already a dictionary, no need to convert it
        pass
    else:
        # If it's a Pydantic model, convert it to a dictionary
        book_dict["BookDetails"] = book_dict["BookDetails"].dict()

    # Prepare the update data using the $set operator
    update_data = {"$set": book_dict}

    # Execute the update query
    result = book_db.find_one_and_update(query, update_data)

    if result:
        return {"status": "Ok", "message": "Data have been updated"}
    else:
        return {"status": "Error", "message": "No book found with the provided ID"}
