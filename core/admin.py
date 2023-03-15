from django.contrib import admin
from .models import (Customer, Adress, Workplace, Product, UserInfo,
                    Payment)

admin.site.register(Adress)
admin.site.register(Workplace)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
                    'id',
                    'product_name',
                    'created_date',
                    'installments_dec',
                    'amount_requested',
                    'loan_period',
                    ]

    readonly_fields = [f.name for f in Product._meta.fields if not f.editable]
    readonly_fields.extend([
        'installement_schedule',
        'payments_human',
        'create_schedule',
        'schedule_human'
    ])


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = [
        'created_date',
        ]

    def delete_queryset(self, request, queryset):
        [item.delete() for item in queryset]


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'id']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'id']
