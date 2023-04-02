import csv

from django.core.management.base import BaseCommand

import reviews.models as rm
from users.models import User

DIR = 'static/data/'
FILE_NAMES = [
    'category', 'genre', 'titles', 'genre_title', 'users', 'review', 'comments'
]


def category(objects, reader):
    for obj in reader:
        objects.append(rm.Category(
            id=int(obj['id']),
            name=str(obj['name']),
            slug=str(obj['slug']),
        ))
    rm.Category.objects.bulk_create(objects)


def genre(objects, reader):
    for obj in reader:
        objects.append(rm.Genre(
            id=int(obj['id']),
            name=str(obj['name']),
            slug=str(obj['slug']),
        ))
    rm.Genre.objects.bulk_create(objects)


def titles(objects, reader):
    for obj in reader:
        objects.append(rm.Title(
            id=int(obj['id']),
            name=str(obj['name']),
            year=int(obj['year']),
            category_id=int(obj['category']),
        ))
    rm.Title.objects.bulk_create(objects)


def genre_title(objects, reader):
    for obj in reader:
        objects.append(rm.GenreTitle(
            id=int(obj['id']),
            title_id=int(obj['title_id']),
            genre_id=int(obj['genre_id']),
        ))
    rm.GenreTitle.objects.bulk_create(objects)


def users(objects, reader):
    for obj in reader:
        objects.append(User(
            id=int(obj['id']),
            username=str(obj['username']),
            email=str(obj['email']),
            role=str(obj['role']),
            bio=str(obj['bio']),
            first_name=str(obj['first_name']),
            last_name=str(obj['last_name']),
        ))
    User.objects.bulk_create(objects)


def review(objects, reader):
    for obj in reader:
        objects.append(rm.Review(
            id=int(obj['id']),
            title_id=int(obj['title_id']),
            text=str(obj['text']),
            author_id=int(obj['author']),
            score=int(obj['score']),
            pub_date=obj['pub_date'],
        ))
    rm.Review.objects.bulk_create(objects)


def comments(objects, reader):
    for obj in reader:
        objects.append(rm.Comment(
            id=int(obj['id']),
            review_id=int(obj['review_id']),
            text=str(obj['text']),
            author_id=int(obj['author']),
            pub_date=obj['pub_date'],
        ))
    rm.Comment.objects.bulk_create(objects)


def objects_create(file_name, reader):
    """
    Функция подготавливает данные из .csv файлов
    и импортирует их в базу данных.
    """
    objects = []
    if file_name == 'category':
        category(objects, reader)
    elif file_name == 'genre':
        genre(objects, reader)
    elif file_name == 'titles':
        titles(objects, reader)
    elif file_name == 'genre_title':
        genre_title(objects, reader)
    elif file_name == 'users':
        users(objects, reader)
    elif file_name == 'review':
        review(objects, reader)
    elif file_name == 'comments':
        comments(objects, reader)
    return print(f'Успешно импортированы данные из {file_name}.csv')


class Command(BaseCommand):
    help = 'Импорт данных из csv в БД'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for file_name in FILE_NAMES:
            with open(DIR + file_name + '.csv', encoding='UTF-8') as csvfile:
                reader = csv.DictReader(csvfile)
                try:
                    objects_create(file_name, reader)
                except Exception as error:
                    print(f'{error} в {file_name}')
