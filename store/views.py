from django.shortcuts import render, get_object_or_404
from store.models import Cart

from store.models import Product

def index(request):
    products = Product.objects.all()
    
    return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product.html', context={"product": product})

def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    Cart.objects.get(user=user)