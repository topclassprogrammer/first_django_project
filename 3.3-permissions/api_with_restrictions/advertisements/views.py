from django.contrib.auth.models import AnonymousUser, User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favourites, \
    AdvertisementStatusChoices
from advertisements.permissions import IsOwnerOrReadOnly, IsAvailableToRetrieve
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        """Получение списка объявлений"""
        filter_params = tuple(dict(request.query_params).keys())
        filter_param = filter_params[0] if filter_params else None
        # Если в GET-запросе есть параметр-фильтр 'created_at',
        # то удаляем его постфикс
        if filter_param:
            postfix = ('_after', '_before')
            for el in postfix:
                filter_param = filter_param.replace(el, '')
        available_filter_params = dict(self.filterset_class.get_filters())
        # Если в GET-запросе есть доступный параметр-фильтр,
        # то выполняем фильтрацию
        if filter_param in available_filter_params:
            queryset = self.filter_queryset(self.queryset)
        else:
            open_closed_ads = Advertisement.objects.filter(status__in=(
                AdvertisementStatusChoices.OPEN,
                AdvertisementStatusChoices.CLOSED))
            # Если пользователь не аутентифицирован
            if isinstance(request.user, AnonymousUser):
                draft_ads = Advertisement.objects.none()
            # Если пользователь является администратором
            elif request.user.is_staff is True:
                draft_ads = Advertisement.objects.filter(
                    status=AdvertisementStatusChoices.DRAFT)
            # Если пользователь аутентифицирован
            elif isinstance(request.user, User):
                draft_ads = Advertisement.objects.filter(
                    creator=request.user,
                    status=AdvertisementStatusChoices.DRAFT)
            queryset = open_closed_ads.union(draft_ads)
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def to_favourites(self, request, pk=None):
        """Добавление объявления в избранное"""
        if not Advertisement.objects.filter(id=pk):
            raise ValidationError(f'Объявления с id {pk} нет в базе')
        elif Favourites.objects.filter(
                user_id=request.user.id, advertisement_id=pk):
            raise ValidationError(f'Объявление с id {pk} уже есть в избранном')
        elif request.user.id == Advertisement.objects.get(id=pk).creator.id:
            raise ValidationError('Вы не можете добавлять в избранное '
                                  'свое собственное объявление')
        elif request.user.id != Advertisement.objects.get(id=pk).creator.id \
                and Advertisement.objects.get(id=pk).status == \
                AdvertisementStatusChoices.DRAFT:
            raise ValidationError('Вы не можете добавлять в избранное чужое '
                                  'объявление находящиеся в статусе черновика')

        Favourites.objects.create(user_id=request.user.id, advertisement_id=pk)
        return Response({'message': f'Объявление с id {pk} '
                        f'успешно добавлено в избранное'})

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'retrieve':
            return [IsAvailableToRetrieve()]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
