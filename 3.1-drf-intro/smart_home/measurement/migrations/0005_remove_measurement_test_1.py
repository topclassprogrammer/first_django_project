# Generated by Django 5.0.6 on 2024-07-06 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0004_alter_measurement_test_1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='test_1',
        ),
    ]
