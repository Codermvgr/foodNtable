from django.db import models
from django.contrib.auth.models import User

def restaurant_directory_path(instance, filename):
    """Upload images to 'media/restaurants/{restaurant_name}/'"""
    return f"restaurants/{instance.name}/{instance.name}.{filename.split('.')[-1]}"

def gallery_directory_path(instance, filename):
    """Upload gallery images to 'media/restaurants/{restaurant_name}/gallery/'"""
    return f"restaurants/{instance.restaurant.name}/gallery/{instance.id}.{filename.split('.')[-1]}"

def item_image_path(instance, filename):
    """Upload item images to 'media/restaurants/{restaurant_name}/items/'"""
    return f"restaurants/{instance.restaurant.name}/items/{instance.name}.{filename.split('.')[-1]}"

def category_image_path(instance, filename):
    """Upload category images to 'media/categories/{category_name}/'"""
    return f"categories/{instance.name}/{instance.name}.{filename.split('.')[-1]}"

class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(decimal_places=7, max_digits=9,null=True)
    longitude = models.DecimalField(decimal_places=7, max_digits=9,null=True)
    facilities = models.ManyToManyField(Facility, related_name="restaurants")  # Many-to-Many
    image = models.ImageField(upload_to=restaurant_directory_path, null=True, blank=True)
    about = models.TextField(blank=True, null=True)  # New field for restaurant description
    opens_at = models.TimeField(blank=True,null=True)  # New field for opening time
    closes_at = models.TimeField(blank=True,null=True)
    cuisine_type = models.CharField(max_length=255, blank=True, null=True)
    price_for_two = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to=gallery_directory_path)

    def __str__(self):
        return f"{self.restaurant.name} Gallery"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=category_image_path, null=True, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    category = models.ManyToManyField(Category, related_name="items")  # Many-to-Many
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_veg = models.BooleanField(default=True)
    image = models.ImageField(upload_to=item_image_path, null=True, blank=True)

     
    @property
    def rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0  # Default if no reviews
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.item.name} in {self.restaurant.name} by {self.user.username}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking at {self.restaurant.name} for {self.user.username if self.user else 'Guest'}"
