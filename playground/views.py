import collections
from decimal import Decimal
from gc import collect
from itertools import product
from turtle import title
from typing import Concatenate
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Customer, Order, Product, OrderItem, Collection
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models import Value, F, Func
from django.db.models.functions import Concat
from django.db.models import ExpressionWrapper
from django.db.models import DecimalField
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from django.db import transaction

# Create your views here.
# @transaction.atomic() # حالت اول استفاده از دیکوریتور هست
def say_hello(request):
    # pull data from DB
    # send email
    # transform data
    
    #..........Managers&QuerySets..........
    # query_set = Product.objects.all()
    
    # retrieve data senario 1
    # for product in query_set:
    #     print(product)
    
    # senario 2
    # list(query_set)
    
    # senario 3
    # query_set[0:5]
    
    # better ways are to use querySet methods like .filter() to make complex queries
    # query_set.filter() 
    # we can define multiple filters on querySet
    # query_set.filter().filter()...d
    
    #..........Retrieving Object(s)..........
    # retrieve
    # try:
        # senario1
        # product = Product.objects.get(pk=1)
        #senario2
        # product = Product.objects.all().first()
        # print(f'the product is {product.title}')
    # except ObjectDoesNotExist:
    #     pass
    
    # to check an object is exist in DB or not
    # return boolean value (True|False)
    # bool_ = Product.objects.filter().exists()
    
    #..........Filtering Objects..........
    # filter equal to:
    # query_set = Product.objects.filter(unit_price=20) # input argument is only acceptable when it likes key-value pair
    
    # filter greater or less than to:
    # __gt: greater than, __gte: greater than or eqaul
    # __lt: less than, __lte: less than or eaqual
    # query_set = Product.objects.filter(unit_price__gt=20)
    # list(query_set)
    
    # filter range:
    # query_set = Product.objects.filter(unit_price__range=(20, 30))    
    
    # another type of filters: make a relationship between models
    # query_set = Product.objects.filter(collection__id__range=(2,3))    
    
    # another type of filter: contain string
    # query_set = Product.objects.filter(title__icontains='Coffee')
   
    # another type: startwith
    # query_set = Product.objects.filter(title__startswith='Coffee')
    
    # another type: time filtering
    # query_set = Product.objects.filter(last_update__year=2021)
    
    # boolean filters
    # query_set = Product.objects.filter(description__isnull=True)
    
    #..........Complex lookups using Q-objects..........
    #1
    # query_set = Product.objects.filter(inventory__lt=15, unit_price__lt=25)
    #2
    # query_set = Product.objects.filter(inventory__lt=15).filter(unit_price__lt=25)
    # the above two ways were for AND condition but to make a query for OR condition must use Q-object
    # query_set = Product.objects.filter(Q(unit_price__lt=25) | Q(inventory__lt=15))
    
    #..........Referencing Fields using F objects..........
    # using F objects when you want to compare two fields
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    # using F class to ref related table field
    # query_set = Product.objects.filter(inventory=F('collection_id'))
    
    #...........Sorting..........
    # query_set = Product.objects.all().order_by('title') # ascending sorting
    # query_set = Product.objects.all().order_by('-title') # descending sorting
    # sort based on multiple fields
    # query_set = Product.objects.all().order_by('unit_price', '-title')
    # reverse method for sorting
    # query_set = Product.objects.filter(unit_price__lt=20).order_by('unit_price', '-title').reverse()
    # order_by method returns a querySet as a list
    # query_set = Product.objects.filter(unit_price__lt=20).order_by('title')[0:5]
    # earliest, latest are two method works like order_by but return a single object
    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.latest('unit_price')
    
    #..........Limiting Results..........
    # query_set = Product.objects.all()[:5] # results LIMIT to 5
    # query_set = Product.objects.all()[5:10] # results LIMIT to 5 and OFFSET 5 items
    
    #..........Selecting Fields to Query..........
    # what do we do when we want to retrive subset of fields: using .values() method, 
    # this returns bunch of dictionary objects instead of bunch of object instances
    # query_set = Product.objects.values('title', 'unit_price')
    # get fields from related table
    # query_set = Product.objects.values('id', 'title', 'collection__title')
    # another method is values_list() it returns bunch of tuple objects
    # query_set = Product.objects.values_list('id', 'title')
    
    # practice:
    # query_set = Product.objects. \
                            # filter(id__in = OrderItem.objects.values('product__title'). \
                                # distinct()).order_by('title') # use distinct method to remove duplicate results
                            
    #..........Deferring fields..........
    # we can choose the specific fields we want to retrive from DB with only() method
    # the difference between only() and values() is the only method retrive instance of the Model class
    # but values returns the dictionary of objects, with only method you can't return 
    # the values of a field tht it doesnt set as input into only method 
    # query_set = Product.objects.only('id', 'title')
    # method defer() returns all fields except those set as input ones in it
    # query_set = Product.objects.defer('title', 'description')

    #.........Selecting Related Objects........
    # select_related() used for One2One or One2Many relationship
    # query_set = Product.objects.select_related('collection').all()
    # prefetch_related() used for many2many relationship
    # query_set = Product.objects.prefetch_related('promotions').all()
    # complex query by chaining prefetch_related and select_related method
    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    
    # query_set = Order.objects.select_related('customer'). \
    #     prefetch_related('orderitem_set__product').order_by('-placed_at')[:10]
    
    #..........Aggregating Objects..........
    # it doesnt return a queryset it returns an dict
    # res = Product.objects.aggregate(count=Count('id'))
    # define multiple query
    # res = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    # apply aggregate method on a queryset
    # res = Product.objects.filter(unit_price__lte=25).aggregate(sum_price=Sum('unit_price'))
    
    #..........Annotating Objects..........
    # in annotate method should set an experssion objects as input argument
    # query_set = Customer.objects.annotate(is_new=Value(True))
    # query_set = Customer.objects.annotate(new_id=F('id') + 1)
    
    #..........Calling Database Function..........
    # query_set = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    # the way to set a query_set like above but in a shorter way: using Concat method directly
    # from django.db.models.functions import Concat
    # query_set = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
    
    #..........Grouping Data..........
    # query_set = Customer.objects.annotate(order_count=Count('order_set')) # returns error, order_set field doesnt exist
    # query_set = Customer.objects.annotate(order_count=Count('order'))
    
    #..........Working with Experssion wrappers..........
    # another type of experssion classes is experssionWrapper, we use this class when we want to define complex experssion
    # from django.db.models import ExpressionWrapper
    # query_set = Product.objects.annotate(discounted_price=F('unit_price') * 0.8) # returns error: experssion contains mixed types: Decimal and float
    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # query_set = Product.objects.annotate(discounted_price=discounted_price)
    
    #..........Quering Generic Relationships..........
    # consider we want to retrieve tags of a product with id=1
    # from django.contrib.contenttypes.models import ContentType
    # from store.models import Product
    # from tags.models import TaggedItem
    # first step find content_type_id of product
    # content_type = ContentType.objects.get_for_model(Product)
    # query_set = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=1)
    
    #..........Custom Managers..........
    # how to write better query for previous one: to this end, we should create custom managers
    # for example: TaggedItem.objects.get_tags_for(Product, 1), here get_tags_for() method plays a role of custom manager
    # query_set = TaggedItem.objects.get_tags_for(Product, 1)
    
    #..........Creating objects..........
    # create new collection
    # first solution
    # collection = Collection()
    # collection.title = 'Video Games' # required field
    # collection.featured_product = Product(pk=1) # first way to fill the optional featured_product field
    # collection.featured_product_id = 1 # the second way, in both ways it's necessary, a product with id=1 to have existed
    # collection.save() # insert new record into DB
    
    # second solution
    # collection = Collection.objects.create(title='musics', featured_product_id=2)
    
    # collection_1 = Collection.objects.get(id=11)
    # collection_2 = Collection.objects.get(id=12)
    # collectionList = [collection_1, collection_2]
    
    #..........Updating Objects.........
    # with this way title set empty automatically
    # collection = Collection(pk=11)
    # collection.title = 'games'
    # collection.featured_product_id = 1
    # collection.save()
    
    # another way to update specific field(s)
    # Collection.objects.filter(pk=11).update(featured_product=None)
    
    #...........Deleting Objects..........
    # delete one object at a time 
    # collection= Collection(pk=11)
    # collection.delete()
    
    # delete more than one item at a time
    # Collection.objects.filter(id__gt=10).delete()
    
    #..........Transactions..........
    # aaply multiple changes on DB and save them together 
    # and if even only one change failed then all other changes should be rolled back
    
    # order = Order()
    # order.customer_id = 1
    # order.save()
    
    # item = OrderItem()
    # item.order = order
    # item.product = 1
    # item.quantity = 10
    # item.unit_price = 50
    # item.save()
    
    # now think with above solution when we wabt to save the item and exception error occured suddenly 
    # but in this situation we have an order in DB that doesnt any item(s) in it!!!
    # so to solve this problem
    
    # ...
    
    # حالت دوم میشه استفاده از نوع context manager
    # with transaction.atomic():    
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()
        
    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 10
    #     item.unit_price = 50
    #     item.save()
    
    #...........Executing Raw SQL queries.........
    # Product.objects.raw('SELECT * FROM store_product')
    # raw query set: can not apply methods like filter, annotate etc... on this type of query
    # rawQuerySet = Product.objects.raw('SELECT * FROM store_product')
    
    #another way is 
    from django.db import connection
    # cursor = connection.cursor() # now we have a cursor object
    # cursor.execute()
    # cursor.close()
    
    # with connection.cursor() as cursor:
    #     cursor.execute()
    
    # stored procedure
    # with connection.cursor() as cursor:
    #     cursor.callproc()
    
    return render(request, 'hello.html', context={'name': 'Vahid',})
