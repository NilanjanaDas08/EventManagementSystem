# Generated by Django 5.1.1 on 2024-10-02 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0005_alter_event_posted_by_alter_event_venue_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Event.venue'),
        ),
    ]