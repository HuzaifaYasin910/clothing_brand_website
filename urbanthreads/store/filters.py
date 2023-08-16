from django.db.models import Q
import django_filters
from .models import Men, Women, Boys, Girls

class MenFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method='filter_search_query')

    class Meta:
        model = Men
        fields = []  # Add the fields you want to use for filtering here

    def filter_search_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(article__icontains=value) |
            Q(color__icontains=value) |
            Q(catagory__icontains=value)
        )

class WomenFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method='filter_search_query')

    class Meta:
        model = Women
        fields = []  # Add the fields you want to use for filtering here

    def filter_search_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(article__icontains=value) |
            Q(color__icontains=value) |
            Q(catagory__icontains=value)
        )

class BoysFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method='filter_search_query')

    class Meta:
        model = Boys
        fields = []  # Add the fields you want to use for filtering here

    def filter_search_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(article__icontains=value) |
            Q(color__icontains=value) |
            Q(catagory__icontains=value)
        )

class GirlsFilter(django_filters.FilterSet):
    search_query = django_filters.CharFilter(method='filter_search_query')

    class Meta:
        model = Girls
        fields = []  # Add the fields you want to use for filtering here

    def filter_search_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(article__icontains=value) |
            Q(color__icontains=value) |
            Q(catagory__icontains=value)
        )
