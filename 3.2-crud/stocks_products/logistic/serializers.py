from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['quantity', 'price', 'product']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    # Реализация с update_or_create

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.update_or_create(stock_id=stock.id, product_id=position['product'].id, defaults=position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            StockProduct.objects.update_or_create(stock_id=stock.id, product_id=position['product'].id, defaults=position)
        return stock

    # # Реализация без update_or_create
    #
    # def create(self, validated_data):
    #     positions = validated_data.pop('positions')
    #     stock = super().create(validated_data)
    #     for position in positions:
    #         StockProduct(**position, stock_id=stock.id).save()
    #     return stock
    #
    # def update(self, instance, validated_data):
    #     positions = validated_data.pop('positions')
    #     stock = super().update(instance, validated_data)
    #     for position in positions:
    #         product_in_stock = StockProduct.objects.filter(stock_id=stock.id).\
    #             filter(product_id=position['product'].id)
    #         # Обновляем запись, если продукт есть на складе
    #         if product_in_stock:
    #             StockProduct.objects.filter(stock_id=instance.id).filter(
    #                 product_id=position['product'].id).update(**position)
    #         # Создаем запись, если продукта нет на складе
    #         else:
    #             StockProduct(**position, stock_id=stock.id).save()
    #     return stock



