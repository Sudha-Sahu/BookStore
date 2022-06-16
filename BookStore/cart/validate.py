from .models import Cart
from rest_framework.response import Response


def book_validator(data):
    bid = data.get('book_id')
    book = Cart.objects.filter(book_id=bid).first()
    if book:
        return Response({'msg': 'Book already exist in cart', 'code': 404})
