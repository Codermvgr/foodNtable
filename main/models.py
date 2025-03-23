from django.db import models
from django.contrib.auth.models import User 
from restaurant.models import Item
# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Table"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profiles/%Y/%m/%d', null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    user_type = models.CharField(choices=[('customer', 'Customer'), ('restaurant', 'Restaurant')], max_length=15, default='customer')
    address = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural="Profile"


# class AddressBook(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address = models.TextField(blank=True, null=True)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     added_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.first_name
class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.latitude}, {self.longitude}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
