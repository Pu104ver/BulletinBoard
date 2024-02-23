import django_filters
from .models import Ad



class ResponseFilter(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, **kwargs):
        super(ResponseFilter, self).__init__(data=data, queryset=queryset, **kwargs)
        if request:
            user = request.user  # Получаем текущего пользователя из запроса
            self.filters['ads'].queryset = Ad.objects.filter(responses__ad__user_profile=user.userprofile).distinct()

    ads = django_filters.ModelChoiceFilter(
        field_name='ad',
        queryset=Ad.objects.none(),  # Начальный queryset, который будет заменен в __init__
        label='Объявления',
    )

    class Meta:
        model = Ad
        fields = {}



