from rest_framework.views import APIView, Response
from cart.models import Cart
from django.contrib.auth.models import User
from book.models import Book
from .models import PlaceOrder
from .serializer import CheckoutSerializer
from utils import decode_token


class CheckoutAPIView(APIView):
    def post(self, request, cid):
        user_id = decode_token(request)
        user = User.objects.get(id=user_id)
        print(user_id)
        if not user:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        cart = Cart.objects.get(id=cid)
        print(cart.book_id)
        book = Book.objects.get(book_name=cart.book_id)
        print(book)
        data = request.data
        serializer = CheckoutSerializer(data)
        address = serializer.data['address']
        order = PlaceOrder.objects.create(
                                        user_id=user,
                                        book_id=book,
                                        address=address,
                                        quantity=cart.quantity,
                                        total_price=cart.total_price)
        order.save()
        print(order.quantity)
        book.quantity_now -= int(order.quantity)
        book.save()
        cart.delete()
        return Response({'Message': f'order placed for {cart.book_id} and will be delivered at {order.address} soon', 'Code': 200})

