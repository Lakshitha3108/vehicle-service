# Generated by Django 5.1.7 on 2025-04-23 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0008_servicebooking_vehicle_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.servicebooking')),
            ],
            options={
                'verbose_name': 'Payments',
                'verbose_name_plural': 'Payments',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rzp_order_id', models.SlugField()),
                ('amount', models.FloatField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('transaction_at', models.DateTimeField(blank=True, null=True)),
                ('rzp_payment_id', models.SlugField(blank=True, null=True)),
                ('rzp_signature', models.TextField(blank=True, null=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
            ],
            options={
                'verbose_name': 'Transactions',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-id'],
            },
        ),
    ]
