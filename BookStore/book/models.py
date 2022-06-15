from django.db import models
import datetime


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.TextField(max_length=300)
    quantity_now = models.IntegerField()
    book_cover = models.ImageField(upload_to="book/images", default="")
    original_quantity = models.IntegerField()
    ratings = models.IntegerField(default=4)
    db_created = models.DateTimeField(auto_now=True)
    db_updated = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "%s" % self.book_name

    def __repr__(self):
        return f'id :{self.id}, book_name : {self.book_name}'

