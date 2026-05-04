# Пример API-контракта

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

