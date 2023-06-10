from importlib.resources import contents
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class TaggedItemManager(models.Manager):
    def get_tags_for(self, object_type, object_id):
        content_type = ContentType.objects.get_for_model(object_type)
        query_set = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=object_id)
        return query_set

class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.label
    
class TaggedItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # type(video, text, image, product, ...)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #ID
    # this way only works fine when the primaryKey's type of related table define with this format
    object_id = models.PositiveIntegerField()
    
    # to use custom managers
    objects = TaggedItemManager()
    
    # to retrive the actual object by a query from DB
    content_object = GenericForeignKey()