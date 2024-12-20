import re
from parsel import Selector
import requests
from config import log


def get_next_page_url(url: str, next_url: str):
    """
    Constructs the URL for the next page based on the current URL and next page relative path.
    """
    if next_url in "":
        return ""
    elif next_url in "1":
        return requests.get(url, timeout=10).text
    else:
        url = url.replace(url.split("/")[-1], next_url)
        return requests.get(url, timeout=10).text


def get_next_url(selector):
    """
    Extracts the URL for the next page from the current page's selector.
    """
    next_url = selector.xpath("//a[text()='next']/@href").get() or ""
    log.log_message(("next url: ", next_url))
    return next_url


def get_selector_from_url(url):
    """
    Helper function to get a Selector object from a URL.
    """
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        log.log_message(f"Successfully fetched URL: {url}")
    else:
        log.log_error(
            f"Failed to fetch URL: {url}, Status code: {response.status_code}"
        )
    return Selector(text=response.text)


def get_img(selector):
    """
    Extracts the book's image URL from the page.
    """
    img = selector.xpath("//img/@src").get()
    img = img.replace("../../../", "https://books.toscrape.com/")
    log.log_message(f"Extracted image URL: {img}")
    return img


def get_title(selector):
    """
    Extracts the book title from the page.
    """
    title = selector.xpath("//h3/a/@title").get()
    log.log_message(f"Extracted book title: {title}")
    return title


def get_price(selector):
    """
    Extracts the book price from the page.
    """
    price = float(selector.xpath("//p[@class='price_color']/text()").get()[2:])
    log.log_message(f"Extracted book price: {price}")
    return price


def get_stock(selector):
    """
    Extracts the stock availability status from the page.
    """
    stock = (
        selector.xpath("//p[@class='instock availability']/text()").getall()[1].strip()
        or "Out of stock"
    )
    log.log_message(f"Extracted stock status: {stock}")
    return stock


def get_book_link(selector):
    """
    Extracts the URL link to the book's detail page.
    """
    book_link = selector.xpath("//h3/a/@href").get()
    book_link = book_link.replace("../../", "https://books.toscrape.com/catalogue/")
    log.log_message(f"Extracted book link: {book_link}")
    return book_link


def get_book_detail_upc(selector):
    """
    Extracts the book's UPC from the detail page.
    """
    upc = selector.xpath("//tr/td/text()").getall()
    if upc:
        log.log_message(f"Extracted upc: {upc[0]}")
        return upc[0]
    log.log_error("Failed to extract upc.")
    return None


def get_book_detail_type(selector):
    """
    Extracts the book type from the detail page.
    """
    book_type = selector.xpath("//tr/td/text()").getall()[1]
    return book_type


def get_book_detail_availability_number(selector):
    """
    Extracts the availability number of the book.
    """
    availability = selector.xpath("//tr/td/text()").getall()[5]
    availability_number = re.search(r"\((\d+)", availability)
    if availability_number:
        return int(availability_number.group(1))
    return 0


def get_book_detail_number_review(selector):
    """
    Extracts the number of reviews for the book.
    """
    number_review = selector.xpath("//tr/td/text()").getall()[-1]
    return int(number_review)


def get_book_detail_description(selector):
    """
    Extracts the book description from the detail page.
    """
    book_desciption = selector.xpath("//article/p/text()").get()
    return book_desciption


def get_book_details(selector):
    """
    Extract all book details using the provided selector.
    """
    description = get_book_detail_description(selector)
    book_upc = get_book_detail_upc(selector)
    book_type = get_book_detail_type(selector)
    availability_number = get_book_detail_availability_number(selector)
    number_review = get_book_detail_number_review(selector)

    return {
        "description": description,
        "upc": book_upc,
        "type": book_type,
        "availability_number": availability_number,
        "number_review": number_review,
    }
