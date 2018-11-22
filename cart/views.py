from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from products.models import Product 
import json

# Create your views here.

def add_to_cart(request):
    product_id = request.POST['product']  #get the value of the imput with name product from the form
    quantity = int(request.POST['quantity']) #get the value of the imput with name quantity from the form
    
    cart = request.session.get('cart', {}) #get the cart from the session
    cart[product_id] = cart.get(product_id, 0) + quantity #I target the value of the product_id key (cart[product_id]). I add the new quantity. but for that i need to know what the previous cuantity was (cart.get(product_id, 0))
    request.session['cart'] = cart #assign the cart(value) which is have we have just done and assign it to the cart(key) within the session
    return redirect("/")  
    
def view_cart(request):
    cart = request.session.get('cart', {}) #get the cart from the session
    
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
        
    return render(request, "cart/view_cart.html", {'cart_items':cart_items,'cart_total':cart_total})

def remove_from_cart(request):
    product_id = request.POST['product'] #get the id from the POST
    
    cart = request.session.get('cart', {})
    del cart[product_id]  #to delete a key-value from a dictionary by the key***  delete the specif product from the cart
    request.session['cart'] = cart #save changes
    
    return redirect("/cart/view_cart/")
    


    
