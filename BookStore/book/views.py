
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Book
from django.contrib.auth.models import User
from .serializer import BookSerializer, BookListSerializer, GetBookSerializer
from django.core.paginator import Paginator
from utils import decode_token
from .validate import book_validator


class BookAPIView(GenericAPIView):
    serializer_class = BookSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(pk=user_id)
        if not user.is_superuser:
            return Response({"error": " Only Admin is allowed", "code": 404})
        data = request.data
        validated_data = book_validator(data)
        if validated_data:
            book = Book.objects.get(id=data.get('id'))
            book.quantity_now = book.quantity_now + int(data.get('original_quantity'))
            book.save()
            return Response({'Message': 'Book already exist so quantity updated', 'Code': 200})
        book = Book.objects.create(**data, quantity_now=data.get('original_quantity'))
        book.save()
        return Response({'Message': 'New Book added', 'Code': 200})

    def get(self, request, pk=None):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(pk=user_id)
        if not user.is_superuser:
            return Response({"error": " Only Admin is allowed", "code": 404})
        if pk:
            book = Book.objects.get(id=pk)
            serializer = GetBookSerializer(book, many=False)
            return Response({'Data': serializer.data, 'Code': 200})
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({'Data': serializer.data, 'Code': 200})

    def delete(self, request, pk):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(pk=user_id)
        if not user.is_superuser:
            return Response({"error": " Only Admin is allowed", "code": 404})
        book = Book.objects.get(id=pk)
        if not book:
            return Response({'error': 'book not found', 'code': 404})
        if book.quantity_now <= 0:
            return Response({"msg": "required amount of book is unavailable", "code": 404})
        book.quantity_now = book.quantity_now - int(request.data.get('quantity'))
        if book.quantity_now >= 0:
            book.save()
            print(book.quantity_now)
        return Response({'Message': 'quantity of book get reduced', 'Code': 200})

    def put(self, request, pk):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(pk=user_id)
        if not user.is_superuser:
            return Response({"error": " Only Admin is allowed", "code": 404})
        print(request.data)
        book = Book.objects.get(id=pk)
        print(book)
        if not book:
            return Response({'Error': "book not found", 'Code': 404})
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response({'Message': 'book Updated', 'Code': 200})


class GetAllBookList(GenericAPIView):
    def get(self, request):
        user_id = decode_token(request)
        print(user_id)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        book_list = Book.objects.order_by('-ratings')
        serializer = BookListSerializer(book_list, many=True)
        paginator = Paginator(book_list, 2)
        page_number = request.data.get('page')
        page_obj = paginator.get_page(page_number)
        return Response({'msg': "all book list store in db ", "data": serializer.data, "page": str(page_obj)})


