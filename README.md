![yamdb workflow](https://github.com/EmilAbushaev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# yamdb_final
Адрес сервера 158.160.27.140

# Краткое описание финального проекта по API

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории (например: книги, музыка, фильмы).
Произведению может быть присвоен жанр (например: детектив, рок, комедия).
Пользователи могут оставлять текстовые отзывы к произведениям и ставить оценки по десятибальной шкале, которые формируют рейтинг произведения.
Отзывы можно комментировать.

В проекте реализована система ролей:
* **Аноним:**  
может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь (user):**  
может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям, может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор (moderator):**  
те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
* **Администратор (admin):**  
полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* **Суперюзер Django:**  
обладает правами администратора. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

# Используемые технологии и библиотеки:
* Python 3.7
* Django 3.2
* djangorestframework 3.12.4
* PyJWT 2.1.0
* simplejwt 4.7.2
* django-filter 22.1

# Установка и настройки
### Создание и активирование виртуального окружения:
```
python -m venv env
```
```
source venv/Scripts/activate
``` 
### Установка зависимостей:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
### Применение миграций:
```
python3 manage.py migrate
```
### Запуск django сервера:
```
python manage.py runserver
```
# Заполнение базы данных из CSV:
```
python manage.py import
```
# Документация:
`http://127.0.0.1:8000/redoc/`
# Примеры запросов к API:
* Получение списка всех произведений:  
Получить список всех объектов. Права доступа: Доступно без токена.  
Эндпоинт: `/api/v1/titles/`  
Метод GET  
Пример ответа:
```
{
    "count": 32,
    "next": "http://127.0.0.1:8000/api/v1/titles/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Побег из Шоушенка",
            "year": 1994,
            "rating": null,
            "description": null,
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "category": {
                "name": "Фильм",
                "slug": "movie"
            }
        },
        {
            "id": 2,
            "name": "Крестный отец",
            "year": 1972,
            "rating": null,
            "description": null,
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "category": {
                "name": "Фильм",
                "slug": "movie"
            }
        }
    ]
}
```

* Получение списка всех отзывов:  
Получить список всех отзывов. Права доступа: Доступно без токена.  
Эндпоинт: `api/v1/titles/{title_id}/reviews/`  
Метод GET  
Пример ответа:

```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "text": "Ставлю десять звёзд!\n...Эти голоса были чище и светлее тех, о которых мечтали в этом сером, убогом месте. Как будто две птички влетели и своими голосами развеяли стены наших клеток, и на короткий миг каждый человек в Шоушенке почувствовал себя свободным.",
            "author": "bingobongo",
            "score": 10,
            "pub_date": "2023-01-13T00:07:22.597972Z"
        },
        {
            "id": 2,
            "text": "Не привыкай\n«Эти стены имеют одно свойство: сначала ты их ненавидишь, потом привыкаешь, а потом не можешь без них жить»",
            "author": "capt_obvious",
            "score": 10,
            "pub_date": "2023-01-13T00:07:22.597972Z"
        }
    ]
}
```
* Получение данных своей учетной записи:  
Получить данные своей учетной записи Права доступа: Любой авторизованный пользователь  
Эндпоинт: `api/v1/users/me/`  
Метод GET  
Пример ответа:
```
{
    "username": "capt_obvious",
    "email": "capt_obvious@yamdb.fake",
    "first_name": "",
    "last_name": "",
    "bio": "",
    "role": "admin"
}
```
Все примеры запросов в Документации.
# Разработчики:
* **Алексей Бакунов** (Лидер команды)  
Заслуги:  
Произведения, категории, жанры, импорт данных из csv файлов, работа с токеном и подтверждение через e-mail, система рейтинга произведений.
* **Эмиль Абушаев**  
Заслуги:  
Система управления пользователями.
* **Сергей Мазяков**  
Заслуги:  
Система отзывов и комментариев.





