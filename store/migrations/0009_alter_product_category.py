# Generated by Django 5.0 on 2024-08-10 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_product_date_of_parution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('bracelets', 'Bracelets'), ('colliers', 'Colliers'), ('boucles-d-oreilles', "Boucles d'oreilles"), ('bagues', 'Bagues')], max_length=50),
        ),
    ]
