# Generated by Django 4.2.2 on 2023-07-19 06:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adult_size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='undefined size', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Girls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='g_images/')),
                ('name', models.CharField(max_length=30)),
                ('price', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('article', models.CharField(default='-------', max_length=30, unique=True)),
                ('qty', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('color', models.CharField(blank=True, default='None', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Minor_size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='undefined size', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=100)),
                ('city', models.CharField(choices=[('1', 'Lahore'), ('2', 'Islamabad'), ('3', 'Karachi'), ('4', 'Multan'), ('5', 'Quetta'), ('6', 'Peshawar'), ('7', 'Hyderabad')], max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('post_code', models.CharField(max_length=100)),
                ('price', models.CharField(default='0', max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='w_images/')),
                ('name', models.CharField(max_length=30)),
                ('price', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('article', models.CharField(default='-------', max_length=30, unique=True)),
                ('qty', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('color', models.CharField(blank=True, default='None', max_length=30)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.adult_size')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews_g',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='store.girls')),
            ],
        ),
        migrations.CreateModel(
            name='Men',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=30)),
                ('price', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('article', models.CharField(default='-------', max_length=30, unique=True)),
                ('qty', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('color', models.CharField(blank=True, default='None', max_length=30)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.adult_size')),
            ],
        ),
        migrations.AddField(
            model_name='girls',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.minor_size'),
        ),
        migrations.CreateModel(
            name='Boys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='b_images/')),
                ('name', models.CharField(max_length=30)),
                ('price', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('article', models.CharField(default='-------', max_length=30, unique=True)),
                ('qty', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('color', models.CharField(blank=True, default='None', max_length=30)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.minor_size')),
            ],
        ),
    ]