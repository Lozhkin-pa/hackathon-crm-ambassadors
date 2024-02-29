# CRM для Амбассадоров ЯП
[![Code-style/tests](https://github.com/Reagent992/hackathon-crm-ambassadors/actions/workflows/code-style_and_tests.yml/badge.svg)](https://github.com/Reagent992/hackathon-crm-ambassadors/actions/workflows/code-style_and_tests.yml)

- Проект команды №1 в хакатоне Яндекс-Практикума.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

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

## [Miro-проекта](https://miro.com/app/board/uXjVNrJFAZc=/?share_link_id=934438081083)

- Там нарисована Архитектура БД
- и Kanban task tracker

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
| [Django filter](https://pypi.org/project/django-filter/)                                                                                                                           | Библиотека для фильтрации данных в приложениях Django.               |
| [django-cors-headers](https://pypi.org/project/django-cors-headers/)                                                                                                               | Настройка политики безопасности HTTP Headers[CORS]                   |
| [Flake8](https://pypi.org/project/flake8/), [black](https://pypi.org/project/black/), [isort](https://pypi.org/project/isort/), [Pre-commit](https://pypi.org/project/pre-commit/) | Инструменты для поддержания Code-Style в проекте.                    |

## Запуск проекта:

### Запуск проекта для локальной разработки:

1. `git clone https://github.com/Reagent992/hackathon-crm-ambassadors.git`
2. `cd hackathon-crm-ambassadors`
3. `python -m venv .venv`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py runserver`

### Загрузка фикстур(ненастоящий данных) в БД.

[Инструкция в соседнем readme-файле по ссылке](./docs/fixtures.md)

## developers guideline
### Остальное
- Язык комментариев, докстрингов, коммитов - русский.

### Активация pre-commit

- Требуется первичная установка: `pre-commit install` для установки git-хуков в вашем локальном репозитории.
- Далее будет запускаться при попытке сделать `git commit` или `pre-commit`

### Инструкция по вкладу в проект:
1. На вашем компьютере создается новая ветка(от ветки `develop`) с названием например `feature/ambassadors` или `fix/ambassadors`.
   - Пример: находясь в ветке `develop`: `git checkout -b feature/ambassadors`
2. `git push --set-upstream origin develop` Для отправки своей новой ветки на GitHub.
3. Далее разработка ведется в вашей новой ветке.
4. После каждого `git commit` у вас запускается `pre-commit` с линтерами и тестами.
5. Перед созданием PR на GitGub вам нужно подтянуть изменения с основной ветки(`develop`) в свою, локальную.
   - Пример: Находясь в своей ветке `feature/ambassadors` нужно выполнить команду `git pull origin develop`. При появление конфликтов с основной веткой вам надо будет решить их.
6. Оправить свою ветку на GitHub и сделать PR в `develop`.
7. Сообщить об этом в чат ТГ и дождаться код-ревью от членов свой команды.
8. PR будет приниматься со squash commits и удалением принятой ветки с GitHub.
9.  Для дальнейшей работы создаем новую ветку начиная с пункта 1.

## Авторы

- [Miron Sadykov](https://github.com/Reagent992)
- [Natalia Arlazarova](https://github.com/Sic15)
- [Pavel Lozhkin](https://github.com/Lozhkin-pa)
- [Vladislav Kondrashov](https://github.com/thehallowedfire)