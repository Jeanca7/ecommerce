# this function is to make the number of items in the cart appear in the icon in every page
#the name of this function goes in the base.py file, in the templates section, in options, in context_processors
#it also goes in the base.html:
# <li><a href="{% url 'view_cart' %}"><i class="fa fa-shopping-cart"></i> Cart                        
#                         <label class="badge badge-light">{{ items_in_cart }}</label></a>
#                     </li>



def items_in_cart(request):
    cart = request.session.get('cart', {})
    
    count=0
    for quantity in cart.values(): #cart.values() is a list of the values in the cart dictionary
        count += quantity 
    
    return {'items_in_cart': count} 
    