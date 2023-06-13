from multiprocessing import context
from sre_constants import SRE_INFO_LITERAL
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Count
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
# Create your views here.

# this is the basic view function based on the HttpRequest and HttpResponce of Django
# def product_list(request):
    
#     return HttpResponse('you are in product list page')

# def product_detail(request):
    
#     return HttpResponse('you are in product detail page')

# def collection_list(request):
    
#     return HttpResponse('you are in collection list page')

# def collection_detail(request):
    
#     return HttpResponse('you are in collection detail page')

# as second try make view function based on api-view of resframework

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # return Response("you are in product list page")
    

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(data=request.data, instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    # elif request.method == 'PATCH':
    #     serializer = ProductSerializer(data=request.data, instance=product)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({'error': 'product cant be deleted because it is associated with an orderitem'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    # return Response(f"you are in product detail page number {id}")

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data
        # model serializer have method name save() to save instance to DB
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # if serializer.is_valid(raise_exception=True):
        #     serializer.validated_data
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # return Response("you are in collection list page")

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')), pk=pk)
    
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer(data=request.data, instance=collection)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'collection can not be deleted because it contains some products!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # return Response(f"you are in collection detail page number {id}")