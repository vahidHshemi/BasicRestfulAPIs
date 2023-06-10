from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>', views.product_detail),
    path('collections/', views.collection_list),
    path('collections/<int:id>', views.collection_detail)
    
]