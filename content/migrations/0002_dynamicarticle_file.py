# Generated by Django 5.1.2 on 2024-11-15 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicarticle',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='my_articles/'),
        ),
    ]