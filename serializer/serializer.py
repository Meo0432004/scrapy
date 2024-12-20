from model.schema import BookScrap, BookDetails


def serialize_to_book_scrap(
    img: str,
    title: str,
    price: float,
    stock: str,
    book_link: str,
    book_upc: str,
    book_description: str,
    book_type: str,
    availability_number: int,
) -> BookScrap:
    """
    Serializes provided data into a BookScrap instance.
    """
    return BookScrap(
        img=img,
        title=title,
        price=price,
        stock=stock,
        book_link=book_link,
        BookDetails=BookDetails(
            book_upc=book_upc,
            book_description=book_description,
            book_type=book_type,
            availability_number=availability_number,
        ),
    )
