from django.contrib import admin

from .models import Category, Course, Review

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Review)

# Register your models here.
