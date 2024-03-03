# Generated by Django 4.2.10 on 2024-03-01 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ambassadors", "0013_alter_merchmiddle_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="ambassador",
            name="yandex_form",
            field=models.BooleanField(
                default=False, verbose_name="Создан через Яндекс Форму"
            ),
        ),
        migrations.AlterField(
            model_name="ambassador",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AlterField(
            model_name="ambassador",
            name="updated",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Дата последнего изменения"
            ),
        ),
    ]