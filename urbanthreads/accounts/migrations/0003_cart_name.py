# Generated by Django 4.2.3 on 2023-07-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='name',
            field=models.CharField(default=4, max_length=100),
            preserve_default=False,
        ),
    ]