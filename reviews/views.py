from django.shortcuts import render, redirect
from products.views import product_detail
from .forms import ReviewsForm
from products.models import Product

def write_reviews(request, id):
    product = Product.objects.get(pk=id)
    form = ReviewsForm(request.POST)
    reviews = form.save(commit=False)
    reviews.product = product
    reviews.save()
    return redirect("product_detail", id)