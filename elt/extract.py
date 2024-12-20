"""
    Use for extract the data from the book pages
"""

from parsel import Selector
import elt.transform as transform
from serializer.serializer import serialize_to_book_scrap
from config import log


def extract_books(url):
    """
    Main extraction function that goes through pages and extracts book data.
    """

    page = transform.get_next_page_url(url, "1")
    all_query = []
    while True:
        selector = Selector(text=page)
        books = selector.xpath("//ol/li").getall()
        for book in books:
            book_selector = Selector(text=book)
            img = transform.get_img(book_selector)
            title = transform.get_title(book_selector)
            price = transform.get_price(book_selector)
            stock = transform.get_stock(book_selector)
            book_link = transform.get_book_link(book_selector)
            book_detail_selector = transform.get_selector_from_url(book_link)
            book_details = transform.get_book_details(book_detail_selector)

            # convert to book model
            model = serialize_to_book_scrap(
                img,
                title,
                price,
                stock,
                book_link,
                book_details["upc"],
                book_details["description"],
                book_details["type"],
                book_details["availability_number"],
            )
            query = {
                "img": model.img,
                "title": model.title,
                "price": model.price,
                "stock": model.stock,
                "book_link": model.book_link,
                "BookDetails": {
                    "book_upc": model.BookDetails.book_upc,
                    "book_description": model.BookDetails.book_description,
                    "book_type": model.BookDetails.book_type,
                    "availability_number": model.BookDetails.availability_number,
                },
            }
            all_query.append(query)
            log.log_message("\n\n")
        next_url = transform.get_next_url(selector)
        page = transform.get_next_page_url(url=url, next_url=next_url)
        log.log_message(("page: ", page))

        # just run for page 3/50
        if next_url in "page-3.html":
            return all_query
