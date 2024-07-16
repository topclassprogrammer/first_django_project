from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from advertisements.models import AdvertisementStatusChoices


class IsAvailableToRetrieve(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff is True:
            return True
        elif (isinstance(request.user, AnonymousUser) and obj.status ==
              AdvertisementStatusChoices.DRAFT) \
                or (request.user != obj.creator and obj.status ==
                    AdvertisementStatusChoices.DRAFT):
            raise ValidationError(f'Объявления с id {obj.id} находится в '
                                  f'статусе черновика пользователя с ником '
                                  f'{obj.creator.username}. Оно вам пока '
                                  f'недоступно для просмотра')
        return True


class IsOwnerOrReadOnly(BasePermission):
    """Проверка прав владения объектом"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff is True:
            return True
        return request.user == obj.creator

