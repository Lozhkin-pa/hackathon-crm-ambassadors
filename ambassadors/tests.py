from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Course,
    EducationGoal,
    Promo,
)
from core.choices import AmbassadorStatus, ClothingSize, PromoStatus, Sex


class AmbassadorTestCase(TestCase):
    fixtures = [
        "ambassadors/fixtures/ambassador_goal_fixture.json",
        "ambassadors/fixtures/course_goal_fixture.json",
        "ambassadors/fixtures/education_goal_fixture.json",
    ]

    @classmethod
    def setUpTestData(cls):
        """Тестовые данные."""
        cls.ambassador1_telegram = "nickname"
        cls.ambassador1_name = "ФИО"
        cls.ambassador1_status = AmbassadorStatus.PAUSED
        cls.ambassador1_onboarding_status = True
        cls.ambassador1_sex = Sex.M
        cls.ambassador1_county = "Россия"
        cls.ambassador1_city = "Москва"
        cls.ambassador1_address = "ул. Мира д.1"
        cls.ambassador1_index = "16234"
        cls.ambassador1_email = "nick_name@domen.com"
        cls.ambassador1_phone = "+9625522333"
        cls.ambassador1_current_work = "python backend developer"
        cls.ambassador1_education = "Среднее образование"
        cls.ambassador1_blog_link = "https://twitter.com/nickname"
        cls.ambassador1_clothing_size = ClothingSize.M
        cls.ambassador1_foot_size = "40"
        cls.ambassador1_comment = "Комментарий"
        cls.ambassador1_education_goals = EducationGoal.objects.first()
        cls.ambassador1_ambassadors_goals = AmbassadorGoal.objects.first()
        cls.ambassador1_course = Course.objects.first()
        cls.ambassador1_promo = Promo.objects.create(value="PROMOCODE0001")
        cls.ambassador1 = Ambassador.objects.create(
            telegram=cls.ambassador1_telegram,
            name=cls.ambassador1_name,
            status=cls.ambassador1_status,
            onboarding_status=cls.ambassador1_onboarding_status,
            sex=cls.ambassador1_sex,
            country=cls.ambassador1_county,
            city=cls.ambassador1_city,
            address=cls.ambassador1_address,
            index=cls.ambassador1_index,
            email=cls.ambassador1_email,
            phone=cls.ambassador1_phone,
            current_work=cls.ambassador1_current_work,
            education=cls.ambassador1_education,
            blog_link=cls.ambassador1_blog_link,
            clothing_size=cls.ambassador1_clothing_size,
            foot_size=cls.ambassador1_foot_size,
            comment=cls.ambassador1_comment,
            education_goal=cls.ambassador1_education_goals,
            course=cls.ambassador1_course,
            promo=cls.ambassador1_promo,
        )
        cls.ambassador1.ambassadors_goals.add(
            cls.ambassador1_ambassadors_goals
        )

    def test_object_created_with_right_data(self):
        """Объект создался с переданными данными."""
        ambassador = Ambassador.objects.get(telegram=self.ambassador1_telegram)

        self.assertEqual(ambassador.name, self.ambassador1_name)
        self.assertEqual(ambassador.status, self.ambassador1_status)
        self.assertEqual(
            ambassador.onboarding_status, self.ambassador1_onboarding_status
        )
        self.assertEqual(ambassador.sex, self.ambassador1_sex)
        self.assertEqual(ambassador.country, self.ambassador1_county)
        self.assertEqual(ambassador.city, self.ambassador1_city)
        self.assertEqual(ambassador.address, self.ambassador1_address)
        self.assertEqual(ambassador.index, self.ambassador1_index)
        self.assertEqual(ambassador.email, self.ambassador1_email)
        self.assertEqual(ambassador.phone, self.ambassador1_phone)
        self.assertEqual(
            ambassador.current_work, self.ambassador1_current_work
        )
        self.assertEqual(ambassador.education, self.ambassador1_education)
        self.assertEqual(ambassador.blog_link, self.ambassador1_blog_link)
        self.assertEqual(
            ambassador.clothing_size, self.ambassador1_clothing_size
        )
        self.assertEqual(ambassador.foot_size, self.ambassador1_foot_size)
        self.assertEqual(ambassador.comment, self.ambassador1_comment)
        self.assertEqual(
            ambassador.education_goal, self.ambassador1_education_goals
        )
        self.assertEqual(ambassador.course, self.ambassador1_course)
        self.assertEqual(ambassador.promo, self.ambassador1_promo)
        self.assertEqual(ambassador.ambassadors_goals.count(), 1)
        self.assertEqual(
            ambassador.ambassadors_goals.first(),
            self.ambassador1_ambassadors_goals,
        )
        self.assertTrue(type(ambassador.created), datetime),
        self.assertTrue(type(ambassador.updated), datetime),

    def test_unique_id_is_enforced(self):
        """Значение id - уникально."""
        with self.assertRaises(IntegrityError) as cm:
            Ambassador.objects.create(
                id=self.ambassador1.id,
            )
        self.assertEqual(
            str(cm.exception),
            "UNIQUE constraint failed: ambassadors_ambassador.id",
        )

    def test_ambassador_defaults(self):
        """Значения по умолчанию для Амбассадора."""
        obj = Ambassador.objects.create()
        self.assertEqual(obj.status, AmbassadorStatus.ACTIVE)
        self.assertEqual(obj.onboarding_status, False)
        self.assertEqual(obj.sex, Sex.UNKNOWN)
        self.assertEqual(obj.ambassadors_goals.count(), 0)
        self.assertEqual(obj.clothing_size, ClothingSize.UNKNOWN)
        self.assertIsNone(obj.telegram)
        self.assertIsNone(obj.name)
        self.assertIsNone(obj.country)
        self.assertIsNone(obj.city)
        self.assertIsNone(obj.index)
        self.assertIsNone(obj.email)
        self.assertIsNone(obj.phone)
        self.assertIsNone(obj.current_work)
        self.assertIsNone(obj.education)
        self.assertIsNone(obj.blog_link)
        self.assertIsNone(obj.foot_size)
        self.assertIsNone(obj.comment)

    def test_string_representation(self):
        """Тест __str__ модели Ambassador."""
        self.assertEqual(str(self.ambassador1), self.ambassador1.name)

    def test_education_goal_str(self):
        """Тест __str__ модели EducationGoal."""
        self.assertEqual(
            str(self.ambassador1_education_goals),
            self.ambassador1_education_goals.title,
        )

    def test_ambassador_goal_str(self):
        """Тест __str__ модели AmbassadorGoal."""
        self.assertEqual(
            str(self.ambassador1_ambassadors_goals),
            self.ambassador1_ambassadors_goals.title,
        )

    def test_course_str(self):
        """Тест __str__ модели Course."""
        self.assertEqual(
            str(self.ambassador1_course), self.ambassador1_course.title
        )

    def test_promo_str(self):
        """Тест __str__ модели Promo."""
        self.assertEqual(
            str(self.ambassador1_promo), self.ambassador1_promo.value
        )

    def test_promo_status(self):
        """Промокод создается со статусом ACTIVE."""
        obj = Promo.objects.create(value="test")
        self.assertEqual(obj.status, PromoStatus.ACTIVE)
