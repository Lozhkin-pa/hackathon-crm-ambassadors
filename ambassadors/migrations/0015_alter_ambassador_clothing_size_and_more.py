# Generated by Django 4.2.10 on 2024-03-03 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "ambassadors",
            "0014_ambassador_yandex_form_alter_ambassador_created_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="ambassador",
            name="clothing_size",
            field=models.CharField(
                choices=[
                    ("XS", "XS - Экстра-маленький"),
                    ("S", "S - Маленький"),
                    ("M", "M - Средний"),
                    ("L", "L - Большой"),
                    ("XL", "XL - Очень большой"),
                    ("UNKNOWN", "Размер не указан"),
                ],
                default="UNKNOWN",
                max_length=250,
                verbose_name="Размер одежды",
            ),
        ),
        migrations.AlterField(
            model_name="merchmiddle",
            name="size",
            field=models.CharField(
                blank=True,
                choices=[
                    ("XS", "XS - Экстра-маленький"),
                    ("S", "S - Маленький"),
                    ("M", "M - Средний"),
                    ("L", "L - Большой"),
                    ("XL", "XL - Очень большой"),
                    ("UNKNOWN", "Размер не указан"),
                ],
                max_length=250,
                null=True,
                verbose_name="Размер",
            ),
        ),
    ]
