# Generated by Django 5.1.1 on 2024-10-16 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='invoice_id',
            field=models.UUIDField(null=True),
        ),
    ]
