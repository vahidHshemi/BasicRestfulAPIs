from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)
    
class TaggedItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # type(video, text, image, product, ...)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #ID
    # this way only works fine when the primaryKey's type of related table define with this format
    object_id = models.PositiveIntegerField()
    
    # to retrive the actual object by a query from DB
    content_object = GenericForeignKey()