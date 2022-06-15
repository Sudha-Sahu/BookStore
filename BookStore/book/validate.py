from .models import Book
from rest_framework.response import Response


def book_validator(data):
    id = data.get('id')
    book = Book.objects.filter(id=id).first()
    if book:
        return Response({'msg': 'Book already exist', 'code': 404})
