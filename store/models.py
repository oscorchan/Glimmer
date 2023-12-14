from django.db import models

# Create your models here.
'''
Produits:

-Nom
-Prix
-Quantité en stock
-Matériaux 1
-Matériaux 2
-Matériaux 3
-Couleur Or
-Catégorie
-Description
-Image
'''
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    material1 = models.CharField(max_length=50)
    material2 = models.CharField(max_length=50, blank=True)
    material3 = models.CharField(max_length=50, blank=True)
    gold_color = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='products', blank=True, null=True)
    