# Generated by Django 4.1.2 on 2022-10-22 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_rename_colors_product_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='color',
            new_name='colors',
        ),
    ]