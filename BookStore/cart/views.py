
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Cart
from book.models import Book
from django.contrib.auth.models import User
from .serializer import CartSerializer, EditCartSerializer, GetCartSerializer
from utils import decode_token
from .validate import book_validator


class CartAPIView(GenericAPIView):
    serializer_class = CartSerializer

    def post(self, request):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(id=user_id)
        if not user:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        new_book = request.data
        book = Book.objects.get(id=new_book.get('book_id'))
        total_amt = book.price * new_book.get('quantity')
        if not book:
            return Response({'Message': f"invalid bookid {book.id}", 'Code': 404})
        if new_book.get('quantity') > book.quantity_now:
            return Response({'Message': "sorry given quantity is unavailable", 'Code': 404})
        validated_data = book_validator(new_book)
        if validated_data:
            cart = Cart.objects.get(book_id=book)
            cart.quantity = cart.quantity + int(new_book.get('quantity'))
            cart.total_price = book.price * cart.quantity
            cart.save()
            return Response({'Message': 'Book already exist so quantity updated', 'Code': 200})

        cart = Cart.objects.create(
                                    user_id=user,
                                    book_id=book,
                                    book_name=book.book_name,
                                    quantity=new_book.get('quantity'),
                                    price_per_item=book.price,
                                    total_price=total_amt,
                                    image=book.book_cover
                                )
        cart.save()
        return Response({'Message': f'{book} book Added to cart', 'Code': 200})

    def get(self, request):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(id=user_id)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        cart = Cart.objects.filter(user_id=user_id)
        serializer = GetCartSerializer(instance=cart, many=True)
        return Response({'Data': serializer.data, 'Code': 200})

    def patch(self, request, id):
        user_id = decode_token(request)
        print(user_id)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        data = request.data
        serializer = EditCartSerializer(data=data)
        if serializer.is_valid():
            quantity = serializer.data['quantity']
            cart = Cart.objects.get(id=id)
            if not cart:
                return Response({'Message': f"invalid cart {id}", 'Code': 401})
            cart.quantity = quantity
            cart.total_price = cart.book_id.price * quantity
            cart.save()
            return Response({'Message': 'Cart updated', 'Code': 200})

    def delete(self, request, id):
        user_id = decode_token(request)
        print(user_id)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        cart = Cart.objects.get(id=id)
        print(cart.user_id)
        # if cart.user_id != user_id:
        #     return Response({'msg': 'You are not authorised user to make changes', 'code': 404})
        cart.delete()
        return Response({'Message': 'Cart Deleted', 'Code': 200})


