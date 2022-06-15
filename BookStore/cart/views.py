

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Cart
from book.models import Book
from django.contrib.auth.models import User
from .serializer import CartSerializer, EditCartSerializer, GetCartSerializer
from utils import encode_token, decode_token


class CartAPIView(GenericAPIView):
    def post(self, request):
        user_id = decode_token(request)
        print(user_id)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        new_book = request.data
        serializer = CartSerializer(data=new_book)

        if serializer.is_valid():
            dict_data = dict(serializer.data)
            print(dict_data)

            book = Book.objects.get(id=dict_data.get('book_id'))
            if not book:
                return Response({'Message': f"invalid bookid {book.id}", 'Code': 404})
            if dict_data.get('quantity') > book.quantity_now:
                return Response({'Message': "sorry given quantity is unavailable", 'Code': 404})
            total_price = book.price * dict_data.get('quantity')
            cart = Cart.objects.create(
                                    user_id=user_id,
                                    book_id=dict_data.get('book_id'),
                                    book_name=book.book_name,
                                    quantity=dict_data.get('quantity'),
                                    price_per_item=book.price,
                                    total_price=total_price,
                                    image=book.book_cover
                                )
            cart.save()
            return Response({'Message': f'{book} book Added to cart', 'Code': 200})
        return Response({'error': 'give all the required field', 'Code': 200})

    def get(self, request):
        user_id = decode_token(request)
        print(user_id)
        user = User.objects.get(id=user_id)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        cart = Cart.objects.filter(user_id=user_id)
        serializer = GetCartSerializer(instance=cart, many=True)
        # if serializer.is_valid():
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
            cart.total_price = cart.book.price * quantity
            cart.save()
            return Response({'Message': 'Cart updated', 'Code': 200})

    def delete(self, request, id):
        user_id = decode_token(request)
        print(user_id)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        cart = Cart.objects.get(id=id)
        if cart.user_id != user_id:
            return Response({'msg': 'You are not authorised user to make changes', 'code': 404})
        cart.delete()
        return Response({'Message': 'Cart Deleted', 'Code': 200})


