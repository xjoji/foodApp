# Generated by Django 3.2.6 on 2021-08-18 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
