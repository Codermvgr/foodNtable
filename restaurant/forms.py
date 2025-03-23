from django import forms
from .models import Restaurant, Item, Booking, Gallery, Review

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'price', 'is_veg', 'description', 'image']


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review...'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["date", "time", "guests"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "guests": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }
