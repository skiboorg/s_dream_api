from rest_framework import serializers
from .models import *





class OstatokSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ostatok
        fields = '__all__'


class ItemSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSize
        fields = '__all__'





class ItemSerializer(serializers.ModelSerializer):
    size=ItemSizeSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Item
        fields = '__all__'


class WhyWeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = WhyWeItem
        fields = '__all__'

class FaqItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FaqItem
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    # items = ItemSerializer(many=True, read_only=True, required=False)
    why_we_items = WhyWeItemSerializer(many=True, read_only=True, required=False)
    faq_items = FaqItemSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Category
        fields = '__all__'


class ItemShortSerializer(serializers.ModelSerializer):


    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'image',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemShortSerializer(many=False, read_only=True, required=False)
    size = ItemSizeSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, required=False)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        items = obj.items.all()
        total_price = 0

        for i in items:
            total_price += i.price

        obj.total_price = total_price
        obj.save()

        return total_price



