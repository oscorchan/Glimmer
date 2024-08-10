from django.db import models
from django.utils.text import slugify
from shop.settings import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

'''
Produits:
- Nom
- Lien
- Prix
- Quantité en stock
- Matériaux 1
- Matériaux 2
- Matériaux 3
- Couleur Or
- Catégorie
- Description
- Image
'''

class Product(models.Model):
    
    MATERIAL_CHOICES = [
        ('Or', 'Or'),
        ('Argent', 'Argent'),
        ('Platine', 'Platine'),
        ('Acier', 'Acier'),
        ('Rubis', 'Rubis'),
        ('Saphir', 'Saphir'),
        ('Emeraude', 'Emeraude'),
        ('Diamant', 'Diamant'),
        ('Perles', 'Perles'),   
    ]
    
    CATEGORY_CHOICES = [
        ('bracelets', 'Bracelet'),
        ('colliers', 'Collier'),
        ('boucles-d-oreilles', 'Boucles d\'oreilles'),
        ('bagues', 'Bague'),     
    ]
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    material1 = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    material2 = models.CharField(max_length=50, blank=True)
    material3 = models.CharField(max_length=50, blank=True)
    gold_color = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='products')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

'''
Commandes:
- Produit
- Utilisateur
- Quantité
- Commandé (oui ou non)
- Date de la commande
'''

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

'''
Panier:
- Utilisateur
- Articles
'''

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def total_items(self):
        total = 0
        for order in self.orders.all():
            total += order.quantity
        return total

@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
