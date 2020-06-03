from django.urls import path
from .views import Homeview, DeleteCityView

urlpatterns = [
    path('', Homeview, name='home'),
    path('delete/<str:city_name>/', DeleteCityView, name='delete'),
]
