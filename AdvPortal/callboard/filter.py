from django_filters import FilterSet, ModelChoiceFilter
from .models import Advert, Response


class ResponseFilter(FilterSet):
    advert = ModelChoiceFilter(
        queryset=Response.objects.all(),
        lookup_expr='exact',
        label='Объявление',
        empty_label='Все объявления',
        field_name='advert_id'
    )

    class Meta:
        model = Response
        fields = []

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['advert'].queryset = Advert.objects.filter(user=kwargs['request'])
