from django.contrib import admin
from .models import Customer, Adress, Workplace, Product, UserInfo
# Register your models here.

admin.site.register(Adress)
admin.site.register(Workplace)



class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'created_date', 'installments',
                    'amount_requested', 'total_amount', 'loan_period']
    readonly_fields = ['created_date', 'id', 'days_since_create',
                    'total_amount', 'installments',
                    'installement_schedule']


class UserInfoAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'id']

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date', 'id']


admin.site.register(Product, ProductAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Customer, CustomerAdmin)