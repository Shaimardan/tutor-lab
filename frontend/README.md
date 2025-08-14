# Frontend 👻
Перед изучением прочтите [README.md](../README.md) 

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 17.3.1.

## 🔷 Содержание
- [Запуск и прокси](#-запуск-и-прокси)
- [Style Guide](#-style-guide)

## 🔷 Запуск и прокси
Для запуска 
Запуск в зависимости от операционной системы
```sh
  cd ..
  npm run run:frontend
```
Для работы необходимо запустить бэк.


Можно использовать [прокси](./src/proxy.conf.json) для запуска фронта без бэка. Тогда данные будут приходить с тестового стенда, но стоит с осторожностью управлять объектами удаленного сервера

## 🔷 Style Guide
Используем airbnb и prettier.
Для форматирования и проверки используйте
```sh
  cd ..
  npm run format:frontend
 ```

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.
