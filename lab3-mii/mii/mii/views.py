from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


def index(request):
    return render(request, 'lab3/main_page.html')