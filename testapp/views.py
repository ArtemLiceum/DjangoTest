from testapp.models import Organization, Shop
from testapp.serializers import OrganizationSerializer, ShopSerializer
from rest_framework import viewsets


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.prefetch_related('shops')
    serializer_class = OrganizationSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
