# orders/urls.py

from django.urls import path
from .views import order_list, order_create, order_update, order_delete, order_approve

urlpatterns = [
    path('orders/', order_list, name='order_list'),
    path('orders/add/', order_create, name='order_create'),
    path('orders/<int:pk>/edit/', order_update, name='order_update'),
    path('orders/<int:pk>/delete/', order_delete, name='order_delete'),
    path('orders/<int:pk>/approve/', order_approve, name='order_approve'),
]
