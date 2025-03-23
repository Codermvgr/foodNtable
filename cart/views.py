from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from .models import Cart, CartItem, Order, OrderItem
from restaurant.models import Item
import razorpay

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        return None  # Handle cases where the user is not authenticated

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = get_cart(request)
    
    if not cart:
        messages.error(request, "Please log in to add items to the cart.")
        return redirect('login')

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"Added {item.name} to your cart.")
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart = get_cart(request)
    if not cart:
        messages.error(request, "Cart is empty.")
        return redirect('cart')

    cart_item = get_object_or_404(CartItem, cart=cart, item__id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('cart')

def cart_detail(request):
    cart = get_cart(request)
    if not cart:
        messages.error(request, "Cart not found.")
        return redirect('cart')

    client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.RAZOR_PAY_KEY_SECRET)) 
    amount = int(cart.get_total()*100)

    context = {
        'cart': cart,
        'items': cart.items.all(),
        'total': cart.get_total(),
        'razorpay_key': settings.RAZOR_PAY_KEY_ID,
    }

    if amount > 0:
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1}) 
        cart.order_id = payment['id']
        cart.save()
        context['payment'] = payment

    return render(request, 'cart_detail.html', context)

def update_cart_item(request, item_id, action):
    cart = get_cart(request)
    if not cart:
        messages.error(request, "Cart not found.")
        return redirect('cart')

    cart_item = get_object_or_404(CartItem, cart=cart, item__id=item_id)
    
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    
    return redirect('cart')

def pay_on_delivery(request):
    cart = get_cart(request)
    
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # Create an order without payment details (Cash on Delivery)
    order = Order.objects.create(
        customer=cart.user,
        order_id=f"COD-{cart.order_id}",
        payment_status=False,  # Since it's COD, it's unpaid
        status='preparing'
    )
    order.save()

    # Transfer cart items to the order
    for item in cart.items.all():
        OrderItem.objects.create(order=order, item=item.item, quantity=item.quantity)

    # Clear the cart
    cart.items.all().delete()
    cart.delete()

    messages.success(request, "Your order has been placed successfully. Pay on delivery!")
    return render(request, 'payment_successfull.html', {'order_id': order.order_id})

def success(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    payment_signature = request.GET.get('signature')

    cart = get_object_or_404(Cart, order_id=order_id)
    cart.is_paid = True
    cart.save()

    order = Order.objects.create(
        customer=cart.user,
        order_id=order_id,
        payment_id=payment_id,
        payment_signature=payment_signature,
        payment_status=True,
        status='preparing'
    )
    order.save()
    
    for item in cart.items.all():
        OrderItem.objects.create(order=order, item=item.item, quantity=item.quantity)

    cart.items.all().delete()
    cart.delete()

    return render(request, 'payment_successfull.html', {'order_id': order_id})

def failure(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    return render(request, 'payment_failed.html', {'order_id': order_id, 'payment_id': payment_id})

def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order.status = 'cancelled'
    order.save()
    return redirect('cart')



