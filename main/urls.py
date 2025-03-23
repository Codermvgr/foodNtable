from django.urls import path
from .views import  get_user_location, subscribe_newsletter, user_profile, save_location, index, register, check_user_exists, signin, dashboard, user_logout, contact_us, about


urlpatterns = [
    path('',index,name="index"),
    path('contact/',contact_us,name="contact"),
    path('about/',about,name="about"),
    path('register/',register,name="register"),
    path('profile/',user_profile,name="user_profile"),
    path('check_user_exists/',check_user_exists,name="check_user_exist"),
    path('login/', signin, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='logout'),
    path('save-location/', save_location, name="save_location"),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path("get-location/", get_user_location, name="get_user_location"),

]
