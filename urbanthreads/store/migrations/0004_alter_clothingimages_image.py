# Generated by Django 4.2.3 on 2023-12-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_clothing_product_qty_clothingsize_size_qty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothingimages',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
