# Тестовое задание Комтек

## Требования
1. Операционная система Windows 10
2. Установленный на машину Docker актуальной версии
3. Подключение к Интернет

## Запуск сервиса
Для запуска сервиса требуется запустить исполняемый файл "docker-start.cmd". После запуска файла будет собран образ на основании python3.8, установлены все необходимые модули, запущены соответствующие контейнеры.

## Общие указания
Сервис разработан на основании модуля Django 3.2 и модуля django-rest-framework. В качестве базы данных используется PostgreSQL 14.
В процессе сборки образа docker применяются миграции, база данных заполняется тестовыми данными, создается суперпользователь (для доступа в административную панель)

## Административная панель
Административная панель достпна по адресу http://localhost:8000/admin/
Логин - admin
Пароль - admin

## API
Запросы выполняются методом GET
1. Получение полного списка справочников: http://localhost:8000/handbook/
2. Получение списка справочников, актуальных на указанную дату: http://localhost:8000/handbook/<date>/
    Пример: http://localhost:8000/handbook/2022-07-01/
3. Получение списка элементов справочника: http://localhost:8000/handbook/<handbook>/
    Пример: http://localhost:8000/handbook/1/
4. Получение списка элементов справочника по его версии: http://localhost:8000/handbook/<handbook>/<version>/
    Пример: http://localhost:8000/handbook/1/1.1/

## Валидация
Валидация параметра по справочнику осуществляется передачей кода элемента и его значения в параметрах метода GET
    Пример: http://localhost:8000/handbook/1/1.1/?code=el1&value=value1.2