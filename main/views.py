import requests
import json

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from restaurant.models import  Booking, Restaurant, Category,  Review
from main.models import Contact, Profile,UserLocation
from cart.models import Cart, CartItem, Order, OrderItem
from .forms import NewsletterForm
from .models import NewsletterSubscriber

@csrf_exempt
@login_required(login_url='login')
def save_location(request):
    if request.method == "POST":
        addr = request.POST.get('address')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        profile, created = UserLocation.objects.get_or_create(user=request.user)
       
        profile.address = addr
        profile.latitude = lat
        profile.longitude = lon
        profile.save()
        messages.success(request, "Location updated successfully!")
    # Redirect back to the page the user was on
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def index(request):
    context ={}
    cats = Category.objects.all().order_by('name')
    context['categories'] = cats
    reviews = Review.objects.all().order_by('-created_at')
    # print()
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        context['profile'] = profile
    dishes = []
    for cat in cats:
        dishes.append({
            'cat_id':cat.id,
            'cat_name':cat.name,
            'cat_img':cat.image,
            'items':list(cat.items.all().values())
        })
    
    context['menu'] = dishes
    context['reviews'] = reviews
    return render(request,'index.html', context)

def contact_us(request):
    context={}
    if request.method=="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        sub = request.POST.get("subject")
        msg = request.POST.get("message")
        
        obj = Contact(name=name, email=email, subject=sub, message=msg)
        message= f"Name: {name}\nEmail: {email}\nSubject: {sub}\nMessage: {msg}"
        send_mail(F"Contact Form - Food N Table by {name}", message, 'yourfoodntable@gmail.com', ['yourfoodntable@gmail.com'])
        obj.save()
        messages.success(request, f"Dear {name}, Thanks for your time!")

    return render(request,'contact.html', context)

def about(request):
    return render(request,'about.html')



def register(request):
    context={}
    if request.method=="POST":
        #fetch data from html form
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        contact = request.POST.get('number')
        check = User.objects.filter(username=email)
        user_type = request.POST.get('user_type')
        restaurant_name = request.POST.get('restaurant_name')
        print(user_type)
        print(restaurant_name)
        if len(check)==0:
            #Save data to both tables
            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.save()

            profile = Profile.objects.create(user=user, contact_number = contact)
            profile.user_type = user_type
            profile.save()

            if user_type == 'restaurant':
                rest = Restaurant.objects.create(owner=user, name=restaurant_name)
                rest.save()

            messages.success(request, f"User {name} Registered Successfully!")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            if user_type == 'restaurant':
                return redirect('restaurant_detail', restaurant_id=rest.id)
            else:
                return HttpResponseRedirect('/dashboard/')

        else:
            context['error'] = f"A User with this email already exists"

    return render(request,'register.html', context)

def check_user_exists(request):
    email = request.GET.get('usern')
    check = User.objects.filter(username=email)
    if len(check)==0:
        return JsonResponse({'status':0,'message':'Not Exist'})
    else:
        return JsonResponse({'status':1,'message':'A user with this email already exists!'})

def signin(request):
    context={}
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        user_type = request.POST.get('user_type')
        print(user_type)
        if user:
            login(request, user)
            messages.success(request, f"User {user.first_name} Successfully logged in!")
            if user.is_superuser or user.is_staff:
                return HttpResponseRedirect('/admin')
            profile, created = Profile.objects.get_or_create(user=user)
            # Redirect based on user type:
            print(profile.user_type)
            if user_type == 'restaurant' and profile.user_type == 'restaurant':
                rest = Restaurant.objects.get(owner=user)
                return HttpResponseRedirect('/restaurant/{}'.format(rest.id))
            else:
                if user_type == 'restaurent' and profile.user_type == 'customer':
                    messages.error(request, "An error occurred while logging in. Please check your profile.Do not have Restaurant account? Register now!")

                return HttpResponseRedirect('/dashboard/')
        else:
            context.update({'message':'Invalid Login Details!','class':'alert-danger'})

    return render(request,'login.html', context)

@login_required(login_url='login')
def dashboard(request):
    context={}
    user = request.user
    #fetch login user's details
    profile, created = Profile.objects.get_or_create(user=user)
    
    context['profile'] = profile

    #update profile
    if "update_profile" in request.POST:
        print("file=",request.FILES)
        name = request.POST.get('name')
        contact = request.POST.get('contact_number')
        add = request.POST.get('address')
       

        profile.user.first_name = name 
        profile.user.save()
        profile.contact_number = contact 
        profile.address = add 

        if "profile_pic" in request.FILES:
            pic = request.FILES['profile_pic']
            profile.profile_pic = pic
        profile.save()
        messages.success(request, "Profile updated successfully!")
    
    #Change Password 
    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_password')

        check = user.check_password(c_password)
        if check==True:
            user.set_password(n_password)
            user.save()
            login(request, user)
            messages.success(request, 'Password Updated Successfully!')
        else:
            messages.error(request,'Current Password Incorrect!')

    #My Orders 
    if profile.user_type == 'customer':
        orders = Order.objects.filter(customer=user).order_by('-id')
        bookings = Booking.objects.filter(
            user=request.user  
        ).order_by('-date', '-time') 
    else:
        restaurant = Restaurant.objects.get(owner=request.user)
        orders = Order.objects.filter(
            order_items__item__restaurant=restaurant
        ).exclude(status__in=["delivered", "cancelled"]).distinct()   
        bookings = Booking.objects.filter(
            restaurant__owner=request.user,visited=False
        ).order_by('-date', '-time')  
     
        context['restaurant'] = restaurant
    print(orders)
    context['orders']=orders  
    context['bookings'] = bookings
    context['user_type'] = profile.user_type 
    print(orders) 
    print(profile.user_type)
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def user_profile(request):

    user =request.user
    
    restaurant_name = request.COOKIES.get('restaurant_name')
    user_type = request.COOKIES.get('user_type')

    if user_type == 'restaurant' and restaurant_name:
        rest, created = Restaurant.objects.get_or_create(owner=user)
        if created:
            rest.name = restaurant_name
            rest.save()

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        if user_type == 'restaurant':
            profile.user_type = user_type
        profile.save()
        messages.success(request, f"User {user.first_name} Registered Successfully!")
    else:
        messages.success(request, f"User {user.first_name}  Successfully logged in!")
    # Redirect based on user type:
    print(user_type)
    print(profile.user_type)
    if user_type == 'restaurant' and profile.user_type == 'restaurant':
        return HttpResponseRedirect('/restaurant/{}'.format(rest.id))
    else:
        if user_type == 'restaurent' and profile.user_type == 'customer':
            messages.error(request, "An error occurred while logging in. Please check your profile.Do not have Restaurant account? Register now!")
        return HttpResponseRedirect('/dashboard/')
    

def user_logout(request):
    logout(request)
    messages.success(request,"Sucessfully logged out!")
    return HttpResponseRedirect('/')





def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        form = NewsletterForm(request.POST)
        if not NewsletterSubscriber.objects.filter(email=email).exists():
            print(email)
            if form.is_valid() :    
                email = form.cleaned_data['email']            
                form.save()
                messages.success(request, "Successfully subscribed to our newsletter!")
                
                # Sending Confirmation Email
                subject = "Subscription Confirmation - Food N Table"
                message = f"Dear Subscriber,\n\nThank you for subscribing to our Food N Table's newsletter! 🎉\n\nStay tuned for exciting updates, exclusive offers, and the latest news.\n\nBest regards,\nFood N Table Team"
                send_mail(subject, message, 'yourfoodntable@gmail.com', [email])

            else:
                messages.error(request, "Invalid email address. Try again.")
                
        else:
            messages.info(request, "You're already subscribed!")

        return redirect('index')  # Change 'home' to your actual homepage URL name

    return redirect('index')

@login_required(login_url='login')
def get_user_location(request):
    if request.user.is_authenticated:
        try:
            user_location = UserLocation.objects.get(user=request.user)
            return JsonResponse({
                "latitude": str(user_location.latitude),
                "longitude": str(user_location.longitude),
                "address": user_location.address
            }, status=200)
        except UserLocation.DoesNotExist:
            return JsonResponse({"error": "Location not found for user"}, status=404)
    return JsonResponse({"error": "User not authenticated"}, status=401)
