from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Collection
# Create your views here.

# this is the basic view function based on the HttpRequest and HttpResponce of Django
def product_list(request):
    
    return HttpResponse('you are in product list page')

def product_detail(request):
    
    return HttpResponse('you are in product detail page')

def collection_list(request):
    
    return HttpResponse('you are in collection list page')

def collection_detail(request):
    
    return HttpResponse('you are in collection detail page')