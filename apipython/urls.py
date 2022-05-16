from django.urls import path
from . import views

urlpatterns = [
    path('get_quotes_coins', views.request_data_comply, name='data'),
]
