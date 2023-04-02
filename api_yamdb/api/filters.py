from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import Filter

from reviews.models import Title


class TitleFilter(FilterSet):
    category = Filter(field_name='category__slug')
    genre = Filter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = '__all__'
