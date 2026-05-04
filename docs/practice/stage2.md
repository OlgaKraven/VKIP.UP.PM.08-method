# Этап 2. Реализация backend и базы данных

## Задание

На этапе нужно создать базу данных, backend/API или серверные MVC-страницы, seed-данные и базовую авторизацию.

## Что сделать

1. Создать структуру проекта.
2. Настроить `.env` и подключение к БД.
3. Создать таблицы пользователей, ролей, журнала действий и предметных сущностей.
4. Реализовать регистрацию служебных пользователей через seed-данные.
5. Реализовать вход и выход.
6. Реализовать защищённые маршруты.
7. Реализовать CRUD API/контроллеры для минимум 4 сущностей.
8. Добавить backend-валидацию.
9. Добавить обработку ошибок.

## Рекомендуемая структура проекта

```text
web-admin-practice/
├── backend/
│   ├── src/
│   ├── migrations/
│   ├── seed/
│   └── .env.example
├── frontend/
│   └── src/
├── docs/
├── README.md
└── docker-compose.yml
```

Для MVC-проекта структура может быть другой, но в репозитории должны быть видны модели, контроллеры, шаблоны/представления и миграции.

### Пример структуры для Flask

```text
web-admin-practice/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── auth/
│   │   ├── routes.py
│   │   └── forms.py
│   ├── admin/
│   │   ├── routes.py
│   │   └── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/login.html
│   │   └── admin/
│   └── static/
│       ├── css/
│       └── js/
├── migrations/
├── seed.py
├── requirements.txt
├── .env.example
└── run.py
```

Минимальные зависимости Flask-проекта:

```text
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-Login
Flask-WTF
python-dotenv
Werkzeug
psycopg2-binary
```

Запуск Flask-варианта:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
python seed.py
flask --app run.py run --debug
```

## Минимальные API/контроллеры

| Раздел | Операции |
|--------|----------|
| Auth | login, logout, текущий пользователь |
| Users | список, создание, редактирование, блокировка |
| Roles | список ролей, назначение роли |
| Entity 1 | CRUD, поиск, фильтрация |
| Entity 2 | CRUD, поиск, фильтрация |
| Entity 3 | CRUD, поиск, фильтрация |
| Entity 4 | CRUD, поиск, фильтрация |
| Activity log | список, фильтр по дате/пользователю/действию |

Для Flask с Jinja2 эти операции могут быть реализованы не только как JSON API, но и как маршруты страниц: `/admin/products`, `/admin/products/create`, `/admin/products/<id>/edit`, `/admin/products/<id>/delete`.

## Что приложить к итоговым материалам

1. Ссылку на репозиторий.
2. DDL/миграции.
3. Seed-данные.
4. Скриншот успешного входа.
5. Скриншоты ответов API или страниц MVC.
6. Краткое описание выбранного backend-стека.

## Чек-лист этапа 2

| Вопрос | Да/нет | Комментарий |
|--------|:------:|-------------|
| База данных создана? |  |  |
| Есть таблицы `users`, `roles`, `activity_log`? |  |  |
| Есть минимум 4 предметные сущности? |  |  |
| Реализован вход в систему? |  |  |
| CRUD работает на backend? |  |  |
| Ошибки валидации возвращаются корректно? |  |  |
