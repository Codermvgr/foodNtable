from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart_item'),
    path('success/',views.success,name='success'),
    path('failure/',views.failure,name='failure'),
    path('pay_on_delivery/',views.pay_on_delivery,name='pay_on_delivery'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
