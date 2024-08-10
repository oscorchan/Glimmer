from django.shortcuts import render, get_object_or_404, redirect
from store.models import Cart, Order, Product
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def index(request):
    category = request.GET.get('category')
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
        
    context = {
        'products': products,
        'selected_category': category,  # Pour afficher la catégorie sélectionnée, si besoin
    }
    
    sort_order = request.GET.get('sort_order', '')
    min_price = request.GET.get('price_min', '')
    max_price = request.GET.get('price_max', '')
    materials = request.GET.getlist('material', [])
    
    if request.method == 'GET':
        sort_order = request.GET.get('sort_order', sort_order)
        min_price = request.GET.get('price_min', min_price)
        max_price = request.GET.get('price_max', max_price)
        materials = request.GET.getlist('material', materials)
        
        request.session['sort_order'] = sort_order
        request.session['price_min'] = min_price
        request.session['price_max'] = max_price
        request.session['materials'] = materials
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if materials:
        material_queries = [Q(material1=material) | Q(material2=material) | Q(material3=material) for material in materials]
        query = material_queries.pop()
        for item in material_queries:
            query &= item
        products = products.filter(query)

    if sort_order == 'ascending':
        products = products.order_by('price')
    elif sort_order == 'descending':
        products = products.order_by('-price')
    elif sort_order == 'alphabetic':
        products = products.order_by('name')
    elif sort_order == 'non-alphabetic':
        products = products.order_by('-name')
        
    context = {
        "products": products,
        "sort_order": sort_order,
        "min_price": min_price,
        "max_price": max_price,
        "selected_materials": materials
    }
    
    return render(request, 'store/index.html', context=context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product.html', context={"product": product})

@login_required
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product)
    
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()
        
    return redirect(reverse("product", kwargs={"slug": slug}))

@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    is_empty = cart.orders.count() == 0
    
    return render(request, 'store/cart.html', context={"orders": cart.orders.all(), "is_empty": is_empty})

@login_required
def increase_quantity(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.quantity += 1
    order.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.quantity == 1:
        order.delete()
    else:
        order.quantity -= 1
        order.save()

    return redirect('cart')

@login_required
def remove_from_cart(request, order_id):
    Order.objects.filter(id=order_id).delete()
    return redirect('cart')
