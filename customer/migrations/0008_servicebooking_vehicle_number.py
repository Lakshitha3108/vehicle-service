# Generated by Django 5.1.7 on 2025-04-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_alter_servicebooking_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebooking',
            name='vehicle_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
