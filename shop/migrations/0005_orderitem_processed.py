# Generated by Django 5.1.2 on 2024-11-30 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]