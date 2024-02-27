# Generated by Django 4.2.10 on 2024-02-26 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("merch", "0003_alter_merch_options_alter_merch_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="merch",
            name="created",
            field=models.DateField(
                auto_now_add=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AlterField(
            model_name="merch",
            name="updated",
            field=models.DateField(
                auto_now=True, verbose_name="Дата последнего изменения"
            ),
        ),
    ]
