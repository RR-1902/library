from decimal import Decimal

from .models import Book

CART_SESSION_KEY = "bookstore_cart"


def get_cart(session):
    return session.setdefault(CART_SESSION_KEY, {})


def add_to_cart(session, book_id, quantity=1):
    cart = get_cart(session)
    key = str(book_id)
    cart[key] = cart.get(key, 0) + int(quantity)
    session.modified = True


def remove_from_cart(session, book_id):
    cart = get_cart(session)
    cart.pop(str(book_id), None)
    session.modified = True


def clear_cart(session):
    session[CART_SESSION_KEY] = {}
    session.modified = True


def cart_items(session):
    cart = get_cart(session)
    books = Book.objects.filter(id__in=cart.keys())
    rows = []
    total = Decimal("0.00")
    count = 0
    for book in books:
        quantity = int(cart.get(str(book.id), 0))
        line_total = book.price * quantity
        rows.append({"book": book, "quantity": quantity, "line_total": line_total})
        total += line_total
        count += quantity
    return rows, total, count
