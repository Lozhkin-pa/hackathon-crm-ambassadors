# Загрузка данных в БД (фикстуры)

## Загрузка фикстур через скрипт

```bash
cd docs              # Переход в папку docs
load_fixtures.bat    # Для загрузки фикстур в бд через Windows-терминал

# Для загрузки фикстур в бд через bash-терминал
chmod +x load_fixtures.sh  # Назначить скрипт исполняемым
./load_fixtures.sh         # Запустить
```
- Аккаунт суперпользователя из фикстур: login: user@user.com  password: user

## Ручная загрузка

```python
cd docs                 # Переход в папку docs
python manage.py loaddata <path_to_fixture>.json --app=<app_name>
```

## Создание фикстур

```python
python -Xutf8 manage.py dumpdata <app_name>.<model_name> --indent=2 --output docs/fixtures/<file_name>.json
```
-  `-Xutf8` добавляет поддержку русского языка.
-  `--indent=2` делает фикстуру "читаемой".
