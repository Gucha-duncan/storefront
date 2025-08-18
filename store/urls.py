from django.urls import path

from .import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('product-detail/<str:pk>/', views.product_detail, name='product-detail'),
]
