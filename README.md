# MVP CRM-системы для Амбассадоров Яндекс Практикума
[![Code-style/tests](https://github.com/Reagent992/hackathon-crm-ambassadors/actions/workflows/code-style_and_tests.yml/badge.svg)](https://github.com/Reagent992/hackathon-crm-ambassadors/actions/workflows/code-style_and_tests.yml)

Проект команды №1 в хакатоне Яндекс Практикума.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

## Скриншоты проекта
<div style="display: flex; justify-content: space-between; align-items: center;">
<a href="./docs/img/1.1 Изучение данных амбассадора.jpg" style="display: block; margin: 0 auto;">
  <img src="./docs/img/1.1 Изучение данных амбассадора.jpg" alt="Данные амбассадора" width="200"/>
</a>
<a href="./docs/img/1.5 добавить вручную амбассадора.jpg" style="display: block; margin: 0 auto;">
  <img src="./docs/img/1.5 добавить вручную амбассадора.jpg" alt="Данные амбассадора" width="200"/>
</a>
<a href="./docs/img/2.1 Промокоды просомтр.jpg" style="display: block; margin: 0 auto;">
  <img src="./docs/img/2.1 Промокоды просомтр.jpg" alt="Данные амбассадора" width="200"/>
</a>
</div>

## Используемые библиотеки и зависимости

| Библиотека                                                                                                                                                                         | Описание                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [Python 3.10](https://www.python.org/)                                                                                                                                             | Язык программирования Python версии 3.10.                            |
| [Django 4](https://pypi.org/project/Django/)                                                                                                                                       | Основной фреймворк для разработки веб-приложений.                    |
| [DRF](https://pypi.org/project/djangorestframework/)                                                                                                                               | Фреймворк для создания API в приложениях Django.                     |
| [Djoser](https://pypi.org/project/djoser/)                                                                                                                                         | Библиотека для обеспечения аутентификации в Django Rest Framework.   |
| [Gunicorn](https://pypi.org/project/gunicorn/)                                                                                                                                     | WSGI-сервер для запуска веб-приложений Django.                       |
| [Environs[django]](https://pypi.org/project/environs/)                                                                                                                             | Библиотека для управления переменными окружения и хранения секретов. |
| [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)                                                                                                     | Генератор документации и Swagger для API в Django.                   |
| [Pillow](https://pypi.org/project/pillow/)                                                                                                                                         | Библиотека для обработки изображений в Python.                       |
| [Django Notifications](https://github.com/django-notifications/django-notifications) | Уведомления. |
| [Pandas](https://pandas.pydata.org/docs/user_guide/index.html) | Библиотека для обработки и анализа данных. |
| [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) | Библиотека для чтения/записи форматов Office Open XML. |
| [Django filter](https://pypi.org/project/django-filter/)                                                                                                                           | Библиотека для фильтрации данных в приложениях Django.               |
| [django-cors-headers](https://pypi.org/project/django-cors-headers/)                                                                                                               | Настройка политики безопасности HTTP Headers[CORS]                   |
| [Flake8](https://pypi.org/project/flake8/), [black](https://pypi.org/project/black/), [isort](https://pypi.org/project/isort/), [Pre-commit](https://pypi.org/project/pre-commit/) | Инструменты для поддержания Code-Style в проекте.                    |

## Инструкция по сборке и запуску

### Запуск проекта для локальной разработки
1. Необходимо создать и заполнить файл .env (пример .envexample).
2. Создать локальное окружение:
    ```
    python -m venv venv - для Windows
    python3 -m venv venv - для Linux
    ```
3. Запустить локальное окружение:
    ```
    . venv/scripts/activate - для Windows
    . venv/bin/activate - для Linux
    ```
4. Установить зависимости:
    ```
    pip install -r requirements.txt
    ```
5. Необходимо в файле config/settings.py закомментировать строку:
    ```
    CSRF_TRUSTED_ORIGINS = ['https://crm-ambassadors.hopto.org']
    ```
6. Выполнить миграции:
    ```
    python manage.py migrate
    ```
7. Запустить сервис разработчика:
    ```
    python manage.py runserver
    ```
### Запуск проекта в контейнерах
Доступен по localhost:8000
```
docker compose -f docker-compose.yaml up -d
```
### Загрузка фикстур (тестовых данных) в БД.
[Инструкция в соседнем readme-файле по ссылке](./docs/fixtures.md)

## Документация API

* На удаленном сервере: [Swagger](https://crm-ambassadors.hopto.org/api/v1/schema/swagger-ui/#/)
* Локально после запуска: [Swagger](http://127.0.0.1:8000/api/v1/schema/swagger-ui/)
* Из дирректории проекта: [CRM_API.yaml](https://github.com/Lozhkin-pa/hackathon-crm-ambassadors/blob/main/docs/schema/CRM_API.yaml)

## Авторы

- [Miron Sadykov](https://github.com/Reagent992)
- [Natalia Arlazarova](https://github.com/Sic15)
- [Pavel Lozhkin](https://github.com/Lozhkin-pa)
- [Vladislav Kondrashov](https://github.com/thehallowedfire)
