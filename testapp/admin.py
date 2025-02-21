from django.contrib import admin
from testapp.models import Organization, Shop


class ShopInline(admin.TabularInline):  # admin.StackedInline
    model = Shop
    extra = 1  # Количество пустых форм для добавления магазинов


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [ShopInline]