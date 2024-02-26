# Generated by Django 4.2.10 on 2024-02-26 09:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("merch", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="merch",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата создания",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="merch",
            name="updated",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Дата последнего изменения"
            ),
        ),
        migrations.AlterField(
            model_name="merch",
            name="article",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Артикул"
            ),
        ),
        migrations.AlterField(
            model_name="merch",
            name="price",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Цена"
            ),
        ),
        migrations.AlterField(
            model_name="merch",
            name="title",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Название"
            ),
        ),
    ]
