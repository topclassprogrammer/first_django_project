from django_filters import rest_framework as filters, DateFromToRangeFilter, \
    CharFilter, NumberFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    creator = NumberFilter(field_name='creator_id')
    status = CharFilter(field_name='status')
    created_at = DateFromToRangeFilter()
    favourites_by = CharFilter(field_name='favourites__user_id')

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'created_at', 'favourites_by']
