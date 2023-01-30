from django.urls import path, include
from . import views

# from rest_framework import routers

# router = routers.DefaultRouter()

# router.register('search_test', views.CustomerViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    # path('rest_api/', views.restApi.as_view(), name='rest_api'),
    # path('my_customers_list/<int:pk>/update/api_home/', views.api_home, name='api_home'),
    # path('my_customers_list/<int:pk>/update/api_home_cbv', views.CustomerUpdateApiView.as_view(), name='api_home_cbv'),
    path('my_customers_list/<int:pk>/api_update', views.CustomerUpdateFetchApiView.as_view(), name='customer_update'),
    path('search/q', views.SearchApiView.as_view(), name='api_search'),
]

