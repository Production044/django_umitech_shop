# Generated by Django 4.1.2 on 2022-10-15 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_product_color_product_colors'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(default='', max_length=255),
        ),
    ]