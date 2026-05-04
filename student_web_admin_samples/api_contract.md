# Пример контракта маршрутов

Пример проекта реализован как Flask + Jinja2 MVC-приложение. Ниже приведены основные HTML-маршруты админ-панели и REST-аналог, который можно использовать при разработке отдельного API.

## MVC-маршруты

| Метод | URL | Назначение | Роли |
|-------|-----|------------|------|
| GET/POST | `/auth/login` | вход в систему | все |
| GET | `/auth/logout` | выход | авторизованный пользователь |
| GET | `/admin/` | dashboard | все роли |
| GET | `/admin/products` | список товаров, поиск и фильтр | все роли |
| GET/POST | `/admin/products/create` | создание товара | `admin`, `manager` |
| GET/POST | `/admin/products/<id>/edit` | редактирование товара | `admin`, `manager` |
| POST | `/admin/products/<id>/delete` | удаление товара | `admin` |
| GET | `/admin/categories` | список категорий | все роли |
| GET | `/admin/customers` | список клиентов | все роли |
| GET | `/admin/orders` | список заказов | все роли |
| GET | `/admin/users` | пользователи и роли | `admin` |
| GET | `/admin/activity-log` | журнал действий | `admin`, `manager` |

## Auth

| Метод | URL | Назначение |
|-------|-----|------------|
| POST | `/api/auth/login` | вход |
| POST | `/api/auth/logout` | выход |
| GET | `/api/auth/me` | текущий пользователь |

## Users

| Метод | URL | Назначение |
|-------|-----|------------|
| GET | `/api/users` | список пользователей |
| POST | `/api/users` | создание пользователя |
| PATCH | `/api/users/{id}` | редактирование |
| PATCH | `/api/users/{id}/status` | блокировка/разблокировка |

## Entity template

| Метод | URL | Назначение |
|-------|-----|------------|
| GET | `/api/<entity>?q=&page=&status=` | список |
| POST | `/api/<entity>` | создание |
| GET | `/api/<entity>/{id}` | просмотр |
| PATCH | `/api/<entity>/{id}` | редактирование |
| DELETE | `/api/<entity>/{id}` | удаление |

