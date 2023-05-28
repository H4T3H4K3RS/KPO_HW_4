from django.urls import path
from .views import (
    OrderCreateView, OrderProcessingView, OrderDetailView, DishDetailView, MenuView,
    DishListView
)

urlpatterns = [
    path('api/dishes/', DishListView.as_view()),
    path('api/dishes/<int:dish_id>/', DishDetailView.as_view()),
    path('api/orders/create/', OrderCreateView.as_view()),
    path('api/orders/process/<int:order_id>/', OrderProcessingView.as_view()),
    path('api/orders/detail/<int:order_id>/', OrderDetailView.as_view()),
    path('api/menu/', MenuView.as_view()),
]
