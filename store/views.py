from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import*

# Create your views here.

@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializer = ProductsSerializer(product, many= True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):  
    
        product = get_object_or_404(Product, id=pk)
        serializer = ProductsSerializer(product, many=False)
        return Response(serializer.data)
   

@api_view(['GET','PUT'])
def product_update(request, pk):  
    if request.method == 'GET':
        product = get_object_or_404(Product, id=pk)
        serializer = ProductsSerializer(product, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        product = get_object_or_404(Product, id=pk)
        serializer = ProductsSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'DELETE'])
def product_delete(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(
                {"error": "Product cannot be deleted because it is associated with an order."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def collection_list(request):
    collection = Collection.objects.all()
    serializer = CollectionSerializer(collection, many = True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def collection_update(request,pk):
    if request.method == 'GET':
        collection = get_object_or_404(Collection, id=pk)
        serializer = CollectionSerializer(collection, many = False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        collection = get_object_or_404(Collection, id=pk)
        serializer = CollectionSerializer(collection, data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def collection_delete(request,pk):
    if request.method == 'GET':
        collection = get_object_or_404(Collection, id=pk)
        serializer = CollectionSerializer(collection, many = False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        collection = get_object_or_404(Collection, id=pk)
        collection.delete()
        return Response('Collection Deleted')
        
    
