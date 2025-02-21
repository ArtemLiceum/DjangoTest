from testapp.models import Organization, Shop
from testapp.serializers import OrganizationSerializer, ShopSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse, HttpRequest
import csv
from rest_framework.permissions import IsAuthenticated
import logging
from testapp.task import send_shop_update_email
from typing import Any

logger = logging.getLogger("api")


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.prefetch_related('shops')
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='shops_file')
    def shops_file(self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            logger.info(f"Запрос на скачивание файла магазинов для организации {pk}")
            organization = self.get_object()
            shops = organization.shops.filter(is_deleted=False)

            if not shops.exists():
                logger.warning(f"Нет доступных магазинов для организации {pk}")

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="organization_{organization.id}_shops.csv"'

            writer = csv.writer(response)
            writer.writerow(['id', 'name', 'description', 'address', 'index', 'is_deleted'])

            for shop in shops:
                writer.writerow(
                    [shop.id, shop.name, shop.description, shop.address, shop.index, shop.is_deleted]
                )

            logger.info(f"Файл успешно сгенерирован для организации {pk}")
            return response
        except Exception as e:
            logger.error(f"Ошибка при генерации файла магазинов для организации {pk}: {e}")
            return HttpResponse(status=500)


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer: ShopSerializer) -> None:
        shop_id = self.kwargs['pk']
        try:
            logger.info(f"Обновление магазина с ID {shop_id}")
            super().prefetch_related(serializer)
            shop = serializer.instance
            send_shop_update_email(shop.id, 'bedintema@gmail.com')
            logger.info(f"Email о обновлении магазина с ID {shop_id} отправлен")
        except Exception as e:
            logger.error(f"Ошибка при обновлении магазина с ID {shop_id}: {e}")
