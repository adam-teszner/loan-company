from django.contrib import admin
from .models import Customer, Adress, Workplace, Product
# Register your models here.

admin.site.register(Customer)
admin.site.register(Adress)
admin.site.register(Workplace)
# admin.site.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'created_date', 'installments','amount_requested', 'total_amount', 'loan_period']
    readonly_fields = ['created_date', 'id', 'days_since_create', 'total_amount', 'installments', 'installement_schedule']


admin.site.register(Product, ProductAdmin)