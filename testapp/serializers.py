from rest_framework import serializers
from testapp.models import Organization, Shop


class OrganizationSerializer(serializers.ModelSerializer):
    shops = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['name', 'description', 'shops']

    def get_shops(self, obj):
        shops = obj.shops.filter(is_deleted=False)
        return ShopSerializer(shops, many=True).data


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'address', 'index', 'is_deleted']