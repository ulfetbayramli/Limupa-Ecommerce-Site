# Generated by Django 4.2 on 2023-04-09 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_product_version_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_version',
            name='units_sold',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units_sold', models.PositiveIntegerField()),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
                ('product_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product_version')),
            ],
        ),
    ]
