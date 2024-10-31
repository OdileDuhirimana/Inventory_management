from django.urls import path
from .views import product_list, product_create, product_update, product_delete

urlpatterns = [
    path('product/', product_list, name='product_list'),
    path('product/add/', product_create, name='product_create'),
    path('product/<int:pk>/edit/', product_update, name='product_update'),
    path('product/<int:pk>/delete/', product_delete, name='product_delete'),
]
