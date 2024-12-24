"""This schema used to define a structure for the book model"""

from pydantic import BaseModel


class BookDetails(BaseModel):
    """
    Model representing detailed information about a book.
    """

    book_upc: str
    book_description: str
    book_type: str
    availability_number: int


class BookScrap(BaseModel):
    """
    Model representing the scraped information of a book.
    """

    img: str
    title: str
    price: float
    stock: str
    book_link: str
    BookDetails: BookDetails  # Nested BookDetails model
