# Generated by Django 3.2.6 on 2021-08-18 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='profile.png', null=True, upload_to=''),
        ),
    ]
