from testapp.models import Organization, Shop
from testapp.serializers import OrganizationSerializer, ShopSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
import csv
from rest_framework.permissions import IsAuthenticated


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.prefetch_related('shops')
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='shops_file')
    def shops_file(self, request, pk=None):
        organization = self.get_object()
        shops = organization.shops.filter(is_deleted=False)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="organization_{organization.id}_shops.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'description', 'address', 'index', 'is_deleted'])

        for shop in shops:
            writer.writerow(
                [shop.id, shop.name, shop.description, shop.address, shop.index, shop.is_deleted]
            )

        return response


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]
