from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from main import views 
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("", include("main.urls")),
    path("restaurant/", include("restaurant.urls")),
    path('cart/',include("cart.urls")),
    path('accounts/profile/', lambda request: redirect('user_profile')),
    path('accounts/', include('allauth.urls')),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
