# Generated by Django 5.1.2 on 2024-12-06 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_dynamicarticle_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicarticle',
            name='author',
            field=models.CharField(help_text='Автор статьи', max_length=50),
        ),
        migrations.AlterField(
            model_name='dynamicarticle',
            name='content',
            field=models.TextField(blank=True, help_text='Содержимое статьи'),
        ),
        migrations.AlterField(
            model_name='dynamicarticle',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата и время создания статьи'),
        ),
        migrations.AlterField(
            model_name='dynamicarticle',
            name='file',
            field=models.FileField(blank=True, help_text='Файл с содержимым статьи', null=True, upload_to='my_articles/'),
        ),
        migrations.AlterField(
            model_name='dynamicarticle',
            name='rubric',
            field=models.CharField(default='Общая', help_text='Рубрика статьи', max_length=100),
        ),
        migrations.AlterField(
            model_name='dynamicarticle',
            name='title',
            field=models.CharField(help_text='Заголовок статьи', max_length=100),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='address',
            field=models.CharField(default='Адрес предприятия', help_text='Адрес предприятия', max_length=255),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=models.TextField(default='Добро пожаловать на сайт ProffShina.', help_text='Основное содержимое главной страницы'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='legal_address',
            field=models.CharField(default='Юридический адрес', help_text='Юридический адрес предприятия', max_length=255),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='phone',
            field=models.CharField(default='Телефон', help_text='Контактный телефон', max_length=50),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='title',
            field=models.CharField(default='ProffShina', help_text='Название сайта', max_length=100),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='unp',
            field=models.CharField(default='УНП', help_text='УНП предприятия', max_length=50),
        ),
    ]