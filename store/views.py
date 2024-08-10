from django.shortcuts import render, get_object_or_404, redirect
from store.models import Cart, Order, Product
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def index(request):
    # Récupération des filtres depuis les paramètres de l'URL
    category = request.GET.get('category')
    sort_order = request.GET.get('sort_order')
    min_price = request.GET.get('price_min')
    max_price = request.GET.get('price_max')
    materials = request.GET.getlist('material')
    gold_color = request.GET.get('gold_color')

    # Filtrer les produits en fonction des critères sélectionnés
    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if materials:
        material_queries = Q()
        for material in materials:
            material_queries |= Q(material1=material) | Q(material2=material) | Q(material3=material)
        products = products.filter(material_queries)

    if 'Or' in materials:
        if gold_color and gold_color != 'tous':
            products = products.filter(gold_color=gold_color)

    # Tri des produits
    if sort_order == 'ascending':
        products = products.order_by('price')
    elif sort_order == 'descending':
        products = products.order_by('-price')
    elif sort_order == 'alphabetic':
        products = products.order_by('name')
    elif sort_order == 'non-alphabetic':
        products = products.order_by('-name')

    # Contexte pour le template
    context = {
        'products': products,
        'selected_category': category,
        'sort_order': sort_order,
        'min_price': min_price,
        'max_price': max_price,
        'selected_materials': materials,
        'gold_color': gold_color,
    }
    
    return render(request, 'store/index.html', context)

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
    else:
        order.quantity += 1
    order.save()
    
    return redirect(reverse("product", kwargs={"slug": slug}))

@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    orders = cart.orders.all()
    is_empty = not orders.exists()
    
    return render(request, 'store/cart.html', context={"orders": orders, "is_empty": is_empty})

@login_required
def increase_quantity(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.quantity += 1
    order.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.quantity > 1:
        order.quantity -= 1
        order.save()
    else:
        order.delete()

    return redirect('cart')

@login_required
def remove_from_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('cart')
