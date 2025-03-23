from django.contrib import admin
from .models import Restaurant, Item, Gallery, Category,Facility, Review
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Gallery)
admin.site.register(Category)
admin.site.register(Facility)
admin.site.register(Review)
admin.site.site_title = "Food N Table"
admin.site.site_header = "Food N Table | Admin"
