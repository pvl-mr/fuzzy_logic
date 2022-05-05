from django.urls import path

from .views import *

urlpatterns = [
    # path('lab3/', lab3_params, name='home'),
    # path('lab3/res', lab3_result),
    # path('lab3/chartJSON', line_chart_json3, name='line_chart_json'),
    path('lab4/chartJSON', line_chart_json4, name='line_chart_json4'),
    path('lab4/chartJSON_clear_time_series', line_chart_json_clear_time_series, name='line_chart_json_clear_time_series'),
    path('lab4/chartJSON_fuzzy_time_series', line_chart_json_fuzzy_time_series, name='line_chart_json_fuzzy_time_series'),
    path('lab4/chartJSON_tendencies', line_chart_json_tendencies, name='line_chart_json_tendencies'),
    path('lab4/', lab4)
]