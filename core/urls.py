from django.urls import path
from . import views

# app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_customer/add', views.CustomerCreateView.as_view(), name='add_customer'),
    path('custom_create', views.custom_customer, name='custom_create'),
    path('accounts/sign_up', views.RegisterUser.as_view(), name='sign_up'),
    path('my_customers_list', views.CustomerListView.as_view(), name='customer_list'),
    path('my_customers_list/<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('my_customers_list/<int:id>/add_prod', views.AddNewProductView.as_view(), name='add_product'),
    
]