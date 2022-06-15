from django.urls import path
from . import views


urlpatterns = [
    path('', views.CartAPIView.as_view()),
    path('<int:id>', views.CartAPIView.as_view()),
]
