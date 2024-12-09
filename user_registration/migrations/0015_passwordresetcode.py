# Generated by Django 5.1.2 on 2024-11-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0014_tirestorage_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=6)),
                ('expiry_date', models.DateTimeField()),
            ],
        ),
    ]
