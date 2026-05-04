# Минимальный skeleton Flask-админки

## `run.py`

```python
from app import create_app

app = create_app()
```

## `app/__init__.py`

```python
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
```

## Обязательные Flask-разделы

| Раздел | Что реализовать |
|--------|-----------------|
| `auth` | login, logout, текущий пользователь |
| `admin/dashboard` | статистика и последние действия |
| `admin/users` | управление пользователями и ролями |
| `admin/<entity>` | CRUD выбранных сущностей |
| `activity_log` | запись действий администратора |

