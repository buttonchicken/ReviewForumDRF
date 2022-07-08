from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Product)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("created_by", "product_id")
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("written_by", "review_id")
    list_filter = ["rating"]
