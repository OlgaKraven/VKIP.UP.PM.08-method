# Учебный пример административной панели

Полноценный пример проекта для ПМ.08: Flask + Jinja2 + SQLAlchemy, авторизация, роли, dashboard, CRUD-разделы, поиск, фильтры, подтверждение удаления и журнал действий.

Опубликованная версия примера: https://github.com/OlgaKraven/VKIP.UP.PM.08-projectWork

Предметная область примера — интернет-магазин.

## Что реализовано

- вход и выход через Flask-Login;
- роли `admin`, `manager`, `viewer`;
- dashboard со статистикой и последними действиями;
- CRUD-разделы: категории, товары, клиенты, заказы;
- поиск товаров, категорий и клиентов;
- фильтр товаров по статусу и заказов по статусу;
- управление пользователями для роли `admin`;
- журнал действий для входов, выходов и изменений данных;
- seed-данные для быстрой демонстрации.

## Структура проекта

```text
student_web_admin_samples/
├── README.md
├── .env.example
├── requirements.txt
├── run.py
├── seed.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── auth/
│   ├── admin/
│   ├── templates/
│   └── static/
├── database/
│   └── schema.sql
└── docs/
    └── screenshots/
```

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
flask --app run.py run --debug
```

После запуска откройте http://127.0.0.1:5000.

## Тестовые пользователи

| Email | Пароль | Роль |
|-------|--------|------|
| `admin@example.local` | `admin12345` | полный доступ |
| `manager@example.local` | `manager12345` | рабочие разделы без управления пользователями |
| `viewer@example.local` | `viewer12345` | просмотр данных |

## Проверка

1. Войти под `admin@example.local`.
2. Открыть dashboard и убедиться, что карточки статистики заполнены.
3. Создать товар, отредактировать его и удалить с подтверждением.
4. Проверить поиск по товарам и фильтр заказов.
5. Открыть журнал действий и убедиться, что операции записаны.
6. Войти под `manager@example.local` и проверить, что раздел пользователей недоступен.

## Как адаптировать под свой вариант

1. Заменить модели предметной области в `app/models.py`.
2. Обновить CRUD-маршруты в `app/admin/routes.py`.
3. Изменить HTML-шаблоны в `app/templates/admin/`.
4. Обновить `database/schema.sql` и seed-данные.
5. Указать свою предметную область и тестовые данные в README.
