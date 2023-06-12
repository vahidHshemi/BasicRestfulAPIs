from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
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

@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(queryset, many=True, context={'request':request})
    # return Response("you are in product list page")
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    # return Response(f"you are in product detail page number {id}")
    return Response(serializer.data)

@api_view()
def collection_list(request):
    queryset = Collection.objects.all()
    serializer = CollectionSerializer(queryset, many=True)
    # return Response("you are in collection list page")
    return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    # return Response(f"you are in collection detail page number {id}")
    return Response(serializer.data)