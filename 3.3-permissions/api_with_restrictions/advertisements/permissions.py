from rest_framework.permissions import BasePermission

from advertisements.models import AdvertisementStatusChoices, Advertisement, \
    Favourites


class IsOwnerOrReadOnly(BasePermission):
    """Проверка прав владения объектом"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff is True:
            return True
        return request.user == obj.creator


class IsAllowedToAddToFavourites(BasePermission):
    """Проверка права добавления в избранное"""
    def has_permission(self, request, view):
        obj_id = view.kwargs['pk']
        try:
            obj = Advertisement.objects.get(id=obj_id)
        except Advertisement.DoesNotExist:
            return False
        # Если объявление уже есть избранном
        if Favourites.objects.filter(advertisement=obj, user=request.user):
            return False
        # Если не свое собственное объявление и оно не в статусе черновика
        elif request.user != obj.creator and obj.status != \
                AdvertisementStatusChoices.DRAFT:
            return True
