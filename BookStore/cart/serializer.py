from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['book_id', 'quantity']


class GetCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class EditCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity']




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