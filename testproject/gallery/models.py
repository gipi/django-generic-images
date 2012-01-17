from django.db import models
from django.contrib.contenttypes import generic
from django.contrib import admin 

from generic_images.admin import AttachedImagesInline
from generic_images.models import AttachedImage


class Cat(models.Model):
    name = models.CharField(max_length=50)

    gallery = generic.GenericRelation(AttachedImage)

class AdminCat(admin.ModelAdmin):
    inlines = [AttachedImagesInline]

admin.site.register(Cat, AdminCat)
