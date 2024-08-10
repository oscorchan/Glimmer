"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, increase_quantity, decrease_quantity, remove_from_cart, checkout
from django.conf.urls.static import static
from accounts.views import signup, login, logout, compte

from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('product/<str:slug>/', product_detail, name='product'),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', cart, name='cart'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('increase-quantity/<int:order_id>/', increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:order_id>/', decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:order_id>/', remove_from_cart, name='remove_from_cart'),
    path('compte/', compte, name='compte'),
    path('checkout/', checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
