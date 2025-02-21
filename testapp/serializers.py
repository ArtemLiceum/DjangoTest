from rest_framework import serializers
from testapp.models import Organization, Shop
from typing import Any


class OrganizationSerializer(serializers.ModelSerializer):
    shops = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['name', 'description', 'shops']

    def get_shops(self, obj: Organization) -> list[dict[str, Any]]:
        shops = obj.shops.filter(is_deleted=False)
        return ShopSerializer(shops, many=True).data


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'address', 'index', 'is_deleted']
