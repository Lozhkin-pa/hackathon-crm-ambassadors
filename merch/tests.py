from django.db import IntegrityError
from django.test import TestCase

from merch.models import Merch


class MerchTestCase(TestCase):
    fixtures = ["merch/fixtures/merch_fixture.json"]

    @classmethod
    def setUpTestData(cls):
        """Тестовые данные."""
        cls.merch1_title = "title"
        cls.merch1_article = "article"
        cls.merch1_price = 1000
        cls.merch1 = Merch.objects.create(
            title=cls.merch1_title,
            article=cls.merch1_article,
            price=cls.merch1_price,
        )

    def test_object_created_with_right_data(self):
        """Объект создался с переданными данными."""
        merch = Merch.objects.get(title=self.merch1_title)

        self.assertEqual(merch.article, self.merch1_article)
        self.assertEqual(merch.price, self.merch1_price)

    def test_unique_id_is_enforced(self):
        """Значение id - уникально."""
        with self.assertRaises(IntegrityError) as cm:
            Merch.objects.create(
                id=self.merch1.id,
            )
        self.assertEqual(
            str(cm.exception),
            "UNIQUE constraint failed: merch_merch.id",
        )

    def test_merch_defaults(self):
        """Значения по умолчанию для Мерча."""
        obj = Merch.objects.create()
        self.assertEqual(obj.title, "Без названия")
        self.assertEqual(obj.article, "")
        self.assertEqual(obj.price, 0)

    def test_string_representation(self):
        """Тест __str__ модели Merch."""
        self.assertEqual(str(self.merch1), self.merch1.title)
