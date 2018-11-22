from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from products.models import Product
from .forms import MakePaymentForm, OrderForm     #import forms.py  for created for the payment details 
from .models import OrderLineItem
from django.conf import settings
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def get_cart_items_and_total(cart):
    cart_items = []  #create list to store the cart items
    cart_total=0
    
    for product_id, quantity in cart.items():    #for product_id, quantity in the items of the cart
        product = get_object_or_404(Product, pk=product_id)   #get specif product with pk=product_id
        
        cart_items.append({
        'id': product.id,  
        'name': product.name,
        'brand': product.brand, 
        'sku': product.sku,
        'description': product.description,
        'image': product.image,
        'price': product.price,
        'stock': product.stock,
        'quantity': quantity,
        'total': product.price * quantity
        })
        
        cart_total+=quantity*product.price   #total of totals
    return {'cart_items': cart_items, 'cart_total': cart_total}

def checkout(request):
    cart = request.session.get('cart', {}) #get the cart from the session
    
    cart_items_and_total = get_cart_items_and_total(cart)
    
    
    payment_form = MakePaymentForm()
    order_form=OrderForm()
    
    context = {'payment_form':payment_form, 'order_form':order_form, 'publishable': settings.STRIPE_PUBLISHABLE_KEY} 
    context.update(cart_items_and_total)  #context.update the context dictionary  
    
    return render(request, "checkout/view_checkout.html", context)
    
def submit_payment(request):
    
    cart = request.session.get('cart', {}) #get the cart from the session
    cart_items_and_total = get_cart_items_and_total(cart)
    
    
    payment_form = MakePaymentForm(request.POST)
    order_form = OrderForm(request.POST) #get the information from the form subbited and i populate it using OrderForm (form made of the order model)***
    
    if order_form.is_valid() and payment_form.is_valid(): #is valid if i get stripe.id
        
        
         #save the order to the database
        order=order_form.save()
        cart = request.session.get('cart', {}) #get cart from session
        for product_id, quantity in cart.items():
            line_item = OrderLineItem() #I get the OrderLineItem model
            
            #i populate the line_item = OrderLineItem model and send it to the database:
            line_item.product_id = product_id #despite product_id doesn't exist in OrderLineItem model, i created by product_id from the cart(this is a django feature)
            line_item.quantity = quantity #populate the cuantity
            line_item.order = order #populate order
            line_item.save() #save the line_item in the database
        
        
        #grab the money and run
        total = cart_items_and_total['cart_total'] #get total of the cart
        stripe_token=payment_form.cleaned_data['stripe_id'] # cleaned_data gives me the digits of the card 

        try:

            total_in_cent = int(total*100)
            customer = stripe.Charge.create(
                amount=total_in_cent,
                currency="EUR",
                description="Dummy Transaction", 
                card=stripe_token,
            )

        except stripe.error.CardError:
            print("Declined")
            messages.error(request, "Your card was declined!")

        if customer.paid:
            print("Paid")
            messages.error(request, "You have successfully paid")
        
        
        
       
            
        del request.session['cart'] #delete the cart from my session
        return redirect("/") 
    

    