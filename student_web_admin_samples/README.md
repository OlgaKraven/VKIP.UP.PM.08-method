# Учебные заготовки для админ-панели

Папка содержит материалы, которые можно использовать как ориентир при разработке проекта ПМ.08.

## Рекомендуемый минимум проекта

```text
web-admin-practice/
├── README.md
├── .env.example
├── requirements-flask.txt
├── backend/
├── frontend/
├── database/
│   ├── schema.sql
│   └── seed.sql
└── docs/
    ├── screenshots/
    └── api_contract.md
```

## Если выбран Flask

Можно использовать Flask как единый backend + server-rendered frontend:

```text
web-admin-practice/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth/
│   ├── admin/
│   ├── templates/
│   └── static/
├── migrations/
├── seed.py
├── run.py
├── requirements.txt
└── .env.example
```

Минимальный запуск:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app run.py run --debug
```

## Чек-лист готовности

| Блок | Готово |
|------|:-----:|
| Login/logout |  |
| Dashboard |  |
| CRUD минимум 4 сущностей |  |
| Users/roles |  |
| Search/filter/pagination |  |
| Validation |  |
| Activity log |  |
| README запуска |  |
