from django.urls import path

from .import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('product-detail/<str:pk>/', views.product_detail, name='product-detail'),
    path('product-update/<str:pk>/', views.product_update, name='product-update'),
    path('product-delete/<str:pk>/', views.product_delete, name='product-delete'),
    path('collection/', views.collection_list, name='collection-list'),
    path('collection-update/<str:pk>/', views.collection_update, name='collection-update'),
    path('collection-delete/<str:pk>/', views.collection_delete, name='collection-delete'),
]
