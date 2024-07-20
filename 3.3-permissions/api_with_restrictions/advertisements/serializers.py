from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления."""
    creator = UserSerializer(
        read_only=True,)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Создание объекта в БД"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Валидируем входящие данные при создании и обновлении объявления,
        чтобы у пользователя было не больше 10 открытых объявлений"""
        user = self.context['request'].user
        user_status_queryset = Advertisement.objects.filter(
            creator=user, status=AdvertisementStatusChoices.OPEN)
        status_count = user_status_queryset.count()
        if status_count >= 10:
            raise ValidationError('У вас больше 10 открытых объявлений')
        return data
