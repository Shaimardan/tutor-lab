# Backend 🚀
Перед изучением прочтите [README.md](../README.md)

## 🔷 Содержание
- [Запуск](#-Запуск)
- [Style Guide](#-style-guide)
- [Typing](#-typing)
- [Docstrings](#-docstrings)
- [Генерация Openapi](#-gen-openapi)
- [DB](#-database)
- [Тестирование](#-тестирование)


## 🔷 Запуск
Запуск в зависимости от операционной системы
```sh
  cd ..
  npm run run:backend:linux
```
```sh
  cd ..
  npm run run:backend
```

## 🔷 Style Guide
Мы используем [Black](https://github.com/psf/black) для форматирования кода, чтобы обеспечить согласованность во всей кодовой базе.
[Isort](https://pycqa.github.io/isort/) Для сортировки импортов.

Ниже приведены команды для проверки и применения форматирования кода.


В зависимости от операционной систему:
```sh
  cd ..
  npm run format:backend
```
```sh
  cd ..
  npm run format:backend:linux
```


## 🔷 Typing
Используем mypy для анализа:
```sh
  mypy .
```

## 🔷 Docstrings
Для документирования кода мы используем формат docstring от Google.

## 🔷 Gen openapi
После написания / изменении эндпоинтов необходимо запустить генерацию openapi. Команда сгенерирует интерфейсы на фронте для работы с эндпоинтами.
```sh
  cd ..
  npm run gen:api
```
Настроен пайплайн, который проверяет актуальность openapi на уровне МР.

## 🔷 Database

### Админка

Доступ к админке при локальной разработке: http://localhost:8003/

Для доступа:
1. engine Postgresql
2. server like dev-db-postgres (or another container name)

### Миграции

Более подробную информацию о работе с миграциями в проекте можно найти [здесь](alembic/README.md)

## 🔷 Minio
Используем Minio для файлового хранилища.

Админка http://localhost:9090/login/. 
Имя пользователя и пароль, задается .env

## 🔷 Тестирование
Используем pytest для тестирования.

Запуск тестов
```sh
  pytest .
```

## Прочее
