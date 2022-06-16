from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'book_name', 'author', 'publisher', 'price', 'original_quantity', 'book_cover', 'desc', 'ratings']
        required_field = ['id', 'book_name', 'author', 'price', 'original_quantity', 'ratings']


class GetBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'book_name', 'author', 'price', 'ratings', 'book_cover']
