# Generated by Django 5.1.2 on 2024-11-19 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_dynamicarticle_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicarticle',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]