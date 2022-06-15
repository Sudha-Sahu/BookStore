from rest_framework.views import APIView, Response
from cart.models import Cart
from .models import PlaceOrder
from .serializer import CheckoutSerializer
from utils import decode_token


class CheckoutAPIView(APIView):
    def post(self, request, id):
        user_id = decode_token(request)
        if not user_id:
            return Response({'Message': f"invalid userid {user_id}", 'Code': 401})
        cart = Cart.objects.get(id=id)
        data = request.data
        serializer = CheckoutSerializer(data)
        address = serializer.data['address']
        order = PlaceOrder.objects.create(
                                        user_id=user_id,
                                        book_id=cart.book_id,
                                        address=address,
                                        quantity=cart.quantity,
                                        total_price=cart.total_price)
        order.save()
        cart.delete()
        return Response({'Message': f'order placed and will be delivered at {order.address} soon', 'Code': 200})

