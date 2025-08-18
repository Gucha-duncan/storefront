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
   
  

    
    
    