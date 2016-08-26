from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import smart_text

class CategoryProduct(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='store/category_products', null=True, blank=True)
    ordering = models.IntegerField(default=0)
    def __unicode__(self):
        return smart_text(self.name)

class Seller(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='store/restaurants', null=True, blank=True)
    category_product = models.ForeignKey(CategoryProduct, null=True, blank=True)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.name)

class Product(models.Model):
    name = models.CharField(max_length=100)
    #picture = models.ImageField(upload_to='store/products', null=True, blank=True)
    description = models.TextField()
    price = models.FloatField()
    review = models.FloatField(blank=True, null=True)
    seller = models.ForeignKey(Seller, blank=True, null=True)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return smart_text(self.name)
