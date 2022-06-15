from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
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





# def create(self, validated_data):
#     user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
#     # At this point, user is a User object that has already been
#     # saved to the database. You can continue to change its
#     # attributes if you want to change other fields.
#
#     user.first_name = validated_data['first_name']
#     user.last_name = validated_data['last_name']
#     user.save()
#     return user