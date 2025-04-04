# Generated by Django 5.1.4 on 2025-01-20 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bazariApp', '0006_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('Item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazariApp.product')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazariApp.user')),
            ],
        ),
    ]
