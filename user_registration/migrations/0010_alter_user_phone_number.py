# Generated by Django 5.1.2 on 2024-11-13 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0009_alter_user_email_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]