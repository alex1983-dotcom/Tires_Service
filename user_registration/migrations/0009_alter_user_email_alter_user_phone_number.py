# Generated by Django 5.1.2 on 2024-11-13 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0008_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='000000000', max_length=15, unique=True),
            preserve_default=False,
        ),
    ]
