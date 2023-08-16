# Generated by Django 4.2.3 on 2023-07-20 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('store', '0004_reviews_g_user_reviews_w_reviews_m_reviews_b'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='reviews_g',
            name='post',
        ),
        migrations.RemoveField(
            model_name='reviews_g',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reviews_m',
            name='post',
        ),
        migrations.RemoveField(
            model_name='reviews_m',
            name='user',
        ),
        migrations.DeleteModel(
            name='Reviews_b',
        ),
        migrations.DeleteModel(
            name='Reviews_g',
        ),
        migrations.DeleteModel(
            name='Reviews_m',
        ),
    ]
