from django.contrib.auth.models import User, AnonymousUser
from django_filters import rest_framework as filters, DateFromToRangeFilter, \
    CharFilter
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    creator = CharFilter(method='get_creator')
    status = CharFilter(method='get_status')
    created_at = DateFromToRangeFilter()
    favourites_by = CharFilter(method='get_favourites')

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'created_at', 'favourites_by']

    def get_creator(self, queryset, name, value):
        """Просмотр объявлений определенного пользователя"""
        ads_ids = tuple(User.objects.values_list('id', flat=True))
        if int(value) not in ads_ids:
            raise ValidationError(f'Пользователь с id {value} '
                                  f'отсутствует в базе')
        elif self.request.user.is_staff is True:
            return Advertisement.objects.filter(creator_id=value)
        elif self.request.user.id == int(value):
            return Advertisement.objects.filter(
                creator_id=self.request.user.id)
        elif self.request.user.id != int(value):
            return Advertisement.objects.filter(
                creator_id=value, status__in=(
                    AdvertisementStatusChoices.OPEN,
                    AdvertisementStatusChoices.CLOSED))
        elif isinstance(self.request.user, AnonymousUser):
            return Advertisement.objects.filter(status__in=(
                AdvertisementStatusChoices.OPEN,
                AdvertisementStatusChoices.CLOSED))

    def get_status(self, queryset, name, value):
        """Просмотр объявлений с определенным статусом"""
        if value == AdvertisementStatusChoices.DRAFT:
            if isinstance(self.request.user, AnonymousUser):
                return Advertisement.objects.none()
            else:
                return Advertisement.objects.filter(
                    creator=self.request.user, status=value)
        else:
            return Advertisement.objects.filter(status=value)

    def get_favourites(self, queryset, name, value):
        """Просмотр избранных объявлений"""
        ads_ids = tuple(User.objects.values_list('id', flat=True))
        if int(value) not in ads_ids:
            raise ValidationError(f'Пользователь с id {value} '
                                  f'отсутствует в базе')
        elif self.request.user.id != int(value):
            raise ValidationError('Вы не можете просматривать'
                                  ' избранные объявления других пользователей')
        favourite_ads = Advertisement.objects.filter(
            favourites__user_id=int(value))
        if not favourite_ads:
            return ValidationError({'У вас нет объявлений в избранном'})
        queryset = Advertisement.objects.filter(favourites__user_id=int(value))
        return queryset
