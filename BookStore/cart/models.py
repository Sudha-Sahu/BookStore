from django.db import models
from book.models import Book
from django.contrib.auth.models import User


class Cart(models.Model):
    id = models.IntegerField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, unique=True)
    book_name = models.CharField(max_length=30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to="book/images", default="")

    def __str__(self):
        return "%s" % self.id

    def __repr__(self):
        return f'id :{self.id}, book_id : {self.book_id}'

