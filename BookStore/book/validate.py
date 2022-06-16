from .models import Book
from rest_framework.response import Response


def book_validator(data):
    bid = data.get('id')
    book = Book.objects.filter(id=bid).first()
    if book:
        return Response({'msg': 'Book already exist', 'code': 404})
