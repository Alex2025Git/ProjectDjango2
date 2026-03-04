# Проект "Онлайн-обучение" на Django
Проект находится в разработке.

## Содержание
- [Технологии](#технологии)
- [Описание структуры проекта](#описание)
- [Тестирование](#тестирование)

## Технологии

- Python 3.13
- Виртуальное окружение Poetry
- Работа с Git
- Django

## Описание

Реализован backend для онлайн-обучения


Структура проета состоит из:

- Проект Django
  
  - Приложения:
  - [courses](courses)
  - [lessons](lessons)
  - [users](users)

- [requirements.txt](requirements.txt)
- [README.md](README.md)


## Тестирование
Протестированы CRUD для Lesson, Courses и управления подпиской

## Подготовка к запуску проекта:

1. Установите Docker-desktop (for windows).
2. Убедитесь, что Docker запущен и работает.
3. Запуск проекта

**Запуск проекта**

Запустите проект, выполнив команду для запуска в фоновом режиме:
```
docker-compose up -d --build
```
После запуска веб-приложение будет доступно по адресу: http://localhost:8000

**Дополнительные команды:**
- Для просмотра запущенных контейнеров:
```
docker-compose ps
```
Для просмотра логов всех контейнеров:
```
docker-compose logs
```
- Для остановки сервисов и удаления контейнеров:
```
docker-compose down
```

**Проверка redis:**
+ В ответ на команду в терминале возвращает -PONG

``` 
docker-compose exec -it redis redis-cli ping
```

**Проверка celery и celery-beat:** 

``` 
docker-compose exec celery celery -A config inspect active