from django.urls import path

from .views import *

urlpatterns = [
    path('', result, name='home'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]