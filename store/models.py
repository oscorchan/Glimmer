from django.db import models
from django.utils.text import slugify

'''
Produits:

-Nom
-lien
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
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    material1 = models.CharField(max_length=50)
    material2 = models.CharField(max_length=50, blank=True)
    material3 = models.CharField(max_length=50, blank=True)
    gold_color = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='products')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
"""
Commandes:

-Articles
-Utilisateur
-Quantité
-Commandé (oui ou non)
"""




"""
Panier:

-Utilisateur
-Articles
-Commandés (oui ou non)
-Date de la commande
"""