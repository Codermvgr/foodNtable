from django.http import HttpResponseForbidden, HttpResponse, JsonResponse

from django.shortcuts import render, get_object_or_404, redirect

from cart.models import Order
from .models import Category, Restaurant, Item, Gallery,Booking, Review
from .forms import RestaurantForm, ItemForm, BookingForm, GalleryForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from main.models import Profile, UserLocation
from math import radians, cos, sin, asin, sqrt

@login_required
def restaurant_detail(request, restaurant_id):
    """View restaurant details page."""
    if restaurant_id is None:
        restaurant = get_object_or_404(Restaurant, owner=request.user)
    else:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    menu_items = restaurant.menu.all()
    gallery_images = restaurant.gallery.all()
    
    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'gallery_images': gallery_images
    })


def add_item(request, restaurant_id):
    """Add new menu items."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form, 'restaurant': restaurant})


def add_gallery(request, restaurant_id):
    """Add new images to the restaurant gallery."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.restaurant = restaurant
            gallery_item.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = GalleryForm()

    return render(request, 'add_gallery.html', {'form': form, 'restaurant': restaurant})





@login_required(login_url='login')
def add_review(request, item_id):
    """Add a review for an item."""
    item = get_object_or_404(Item, id=item_id)
    restaurant = item.restaurant  # Get the restaurant from the item

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Ensure valid rating
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            messages.error(request, "Invalid rating. Please select a rating between 1 and 5.")
            return redirect("dashboard")

        # Save Review
        Review.objects.create(
            restaurant=restaurant,
            item=item,
            user=request.user,
            rating=int(rating),
            comment=comment,
        )

        messages.success(request, "Your review has been submitted successfully.")
        return redirect("dashboard")  # Redirect to user dashboard after submission

    return redirect("dashboard")
@login_required(login_url='login')
def edit_restaurant(request, restaurant_id):
    """Edit restaurant details including gallery and image."""

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if restaurant.owner != request.user:
        messages.warning(request,"You are not authorized to edit this restaurant.")
        return redirect('restaurant_detail', restaurant_id=restaurant.id)
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)
    
    return render(request, 'edit_restaurant.html', {'form': form, 'restaurant': restaurant})



def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance (in km) between two points 
    on the Earth using the Haversine formula.
    """
    R = 6371  # Radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    print(R*c)
    return R * c  # Distance in km

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    
    if request.user.is_authenticated :
        profile = Profile.objects.get(user=request.user)
        user_location, created = UserLocation.objects.get_or_create(user=request.user)
        if created or not user_location.latitude or not user_location.longitude:
            messages.success(request, "Please update your location to get restaurants near you.")
        elif user_location.latitude and user_location.longitude and profile.user_type == 'customer':
            user_lat = float(user_location.latitude)
            user_lon = float(user_location.longitude)

           # Filter restaurants within a 20 km range
            restaurants = [
                restaurant for restaurant in restaurants 
                if restaurant.latitude is not None and restaurant.longitude is not None and
                haversine(user_lat, user_lon, float(restaurant.latitude), float(restaurant.longitude)) <= 40
            ]


    return render(request, 'restaurants.html', {'restaurants': restaurants})


def book_table(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.restaurant = restaurant
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            messages.success(request, "Your table has been booked successfully!")
            return redirect("dashboard")
    else:
        form = BookingForm()

    return render(request, "book_table.html", {"form": form, "restaurant": restaurant})


def all_dishes(request):
    context = {}
    dishes = Item.objects.all()

    # Search Functionality
    query = request.GET.get("q")
    if query:
        dishes = Item.objects.filter(
            Q(name__icontains=query) |  # Search by dish name
            Q(restaurant__name__icontains=query) |  # Search by restaurant name
            Q(category__name__icontains=query)  # Search by category name
        ).distinct()
    
    # Filter by Category ID
    category_id = request.GET.get("category")
    if category_id:
        dishes = dishes.filter(category__id=category_id)
        context['dish_category'] = Category.objects.get(id=category_id).name 

    context['dishes'] = dishes
    return render(request, 'all_dishes.html', context)


def single_dish(request, id):
    context={}
    request.session['dishId'] = id
    dish = get_object_or_404(Item, id=id)

    print(dish)

    if request.user.is_authenticated:
        user = request.user


        form = ''
        context.update({'dish':dish, 'form':form})

    return render(request,'dish.html', context)



@login_required
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
    return redirect("dashboard")  # Redirect to order history




@login_required
def update_booking_status(request, booking_id):

    print(booking_id)
    booking = get_object_or_404(Booking, id=booking_id)

    # Ensure only the restaurant owner can update the booking
    if request.user != booking.restaurant.owner:
        print("You are not allowed to update this booking.")
        return HttpResponseForbidden("You are not allowed to update this booking.")

    if request.method == "POST":
        status = request.POST.get("visited")
        print(status)
        # Example status update (mark as visited)
        if status == "true":
            booking.visited = True
        else:
            booking.visited = False

        booking.save()
    return redirect("dashboard")  # Change to your appropriate redirect URL

