from django.contrib import admin
from .models import Cart,CartItem,Order,OrderItem
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.site_title = "Food N Table"
admin.site.site_header = "Food N Table | Admin"