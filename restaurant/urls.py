from django.urls import path
from . import views

urlpatterns = [

    path('<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('<int:restaurant_id>/add-item/', views.add_item, name='add_item'),
    path('<int:restaurant_id>/add-gallery/', views.add_gallery, name='add_gallery'),
    path('<int:restaurant_id>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path('<int:restaurant_id>/book_table/', views.book_table, name="book_table"),
    path('dishes/',views.all_dishes,name="all_dishes"),
    path('dish/<int:dish_id>/', views.single_dish, name='dish'),
    path('all/', views.restaurant_list, name='restaurants'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path("update-booking-status/<int:booking_id>/", views.update_booking_status, name="update_booking_status"),
    path("add_review/<int:item_id>/", views.add_review, name="add_review"),

]

