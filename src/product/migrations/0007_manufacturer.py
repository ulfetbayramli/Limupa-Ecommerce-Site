# Generated by Django 4.2 on 2023-04-08 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Product Manufacturer',
                'verbose_name_plural': 'Product Manufacturers',
            },
        ),
    ]
