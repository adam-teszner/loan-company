from django.urls import path
from . import views


urlpatterns = [
    path('my_customers_list/<int:pk>/api_update',
            views.CustomerUpdateFetchApiView.as_view(),
            name='customer_update'),
    path('search/q', views.SearchApiView.as_view(), name='api_search'),
    path('search/p', views.GeneratePDFView.as_view(), name='generate_pdf')
]
