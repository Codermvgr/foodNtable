from django.db import models
from django.conf import settings
from django.utils import timezone
from restaurant.models import Item


# Cart model: optionally linked to a logged-in user or session key
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    
    order_id = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart ({self.pk})"

    def get_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total

# CartItem model: represents an item in the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def get_total_price(self):
        return self.item.price * self.quantity



class Order(models.Model):
    STATUS_CHOICES = [
        ('cancelled', 'Cancelled'),
        ('preparing', 'Preparing'),
        ('on_the_way', 'On The Way'),
        ('delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_signature = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cancelled')
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.customer.username}"

    
    def get_total(self):
        return sum(order_item.get_total_price() for order_item in self.order_items.all())



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    
    def get_total_price(self):
        return self.item.price * self.quantity
