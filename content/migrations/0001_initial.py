# Generated by Django 5.1.2 on 2024-10-27 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rubric', models.CharField(default='Общая', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='ProffShina', max_length=100)),
                ('content', models.TextField(default='Добро пожаловать на сайт ProffShina.')),
                ('address', models.CharField(default='Адрес предприятия', max_length=255)),
                ('phone', models.CharField(default='Телефон', max_length=50)),
                ('unp', models.CharField(default='УНП', max_length=50)),
                ('legal_address', models.CharField(default='Юридический адрес', max_length=255)),
            ],
        ),
    ]
