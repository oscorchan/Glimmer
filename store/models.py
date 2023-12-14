from django.db import models

# Create your models here.
'''
Produits:

-Nom
-Prix
-Quantité en stock
-Matériaux
-Catégorie
-Description
-Image
'''

class Material(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_lenght=50)
    price = models.DecimalField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    materials = models.ManyToManyField(Material)
    category = models.CharField(max_lenght=50)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='products', blank=True, null=True)
    