from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline

from tags.models import TaggedItem
from . import models
# Register your models here.
# admin.site.register(models.Collection)
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    # Overriding Base QuerySet
    list_display = ['title', 'products_count']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # Providing Links to Other Pages
        url = (reverse('admin:store_product_changelist')
                      + '?'
                      + urlencode({
                          'collection__id':str(collection.id)
                      }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )
        
    # searchFiled for autocmpleteField in ProductAdmin
    search_fields = ['title']

# Customize filtering
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
            ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
    
# class TagInline(GenericTabularInline):
#     model = TaggedItem
#     autocomplete_fields = ['tag']

# admin customization
# customizing list page
@admin.register(models.Product) # shorter way to register product model in admin panel
class ProductAdmin(admin.ModelAdmin):
    # list_display = ['title', 'unit_price', 'inventory']
    # list_display = ['title', 'unit_price', 'inventory_status']
    # selecting related objects
    # list_display = ['title', 'unit_price', 'inventory_status', 'collection'] # display collection column as string representation
    # with above display method we cant point to the specific field of related table: 'collection__title' return error
    # so we need to define new method in ProductAdmin class
    @admin.display(ordering='collection') # the problem of this way is send extra queries to DB and bad performance
    def collection_title(self, Product):
        return Product.collection.title
    
    list_select_related = ['collection'] # use preloading to optimize performance
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    
    list_editable = ['unit_price']    
    list_per_page = 50
    
    # Adding Computed columns and set ordering based oninventory
    @admin.display(ordering='inventory')
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return 'LOW'
        else:
            return 'OK'
    
    # Adding Filtering to the list page
    list_filter = ['collection', 'last_update', InventoryFilter]
    
    # Creating Custome actions
    actions = ['clear_inventory']
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        
        self.message_user(request,
                          f'{update_count} products were successfully updated!',
                          messages.ERROR)
    
    # Customizing forms
    # fields: Optional[_FieldGroups] # determines which fields will be shown to the user
    # exclude: Optional[Sequence[str]] # sets fields that will not be shown to the user
    # readonly_fields: Sequence[str] # these fields cant change by user
    # automatically fill a field by the value of other(s) field(s): use prepopulated_fields attribute
    prepopulated_fields = {'slug': ('title',)}
    
    # autocompleteFileds
    autocomplete_fields = ['collection']
    
    #searchfield for orderitem
    search_fields = ['title']
    
    # inline fields
    # inlines = [TagInline]
    
    
    
# another way to register Product model is:
# admin.site.register(models.Product, ProductAdmin)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist') 
               + '?' 
               + urlencode({
                   'customer__id': str(customer.id)
               }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)
        # return order.orders_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )
    
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    
    # Adding Search to the list page
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    list_per_page = 20
    

class OrderItemsInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    
    # Editing Children using inlines
    inlines = [OrderItemsInline]
    
    list_per_page = 10