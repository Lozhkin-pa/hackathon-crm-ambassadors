# Generated by Django 4.2.10 on 2024-02-26 15:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего изменения"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Уникальный идентификатор",
                    ),
                ),
                (
                    "platform",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Площадка размещения контента",
                    ),
                ),
                (
                    "link",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Ссылка на контент",
                    ),
                ),
                (
                    "file",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Ссылка на файл",
                    ),
                ),
                (
                    "guide",
                    models.BooleanField(
                        default=False, verbose_name="Контент в рамках гайда"
                    ),
                ),
            ],
            options={
                "verbose_name": "Контент",
                "verbose_name_plural": "Контент",
                "ordering": ("-created",),
            },
        ),
    ]
