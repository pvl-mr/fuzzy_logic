from random import random

from chartjs.views.lines import BaseLineChartView
from django.shortcuts import render
import random, math
from django.views.generic import TemplateView

count_clusters = 4
zp = [random.randint(30, 300) for i in range(100)]
clusters = [0 for i in range(count_clusters)]
u = [[random.random() for i in range(count_clusters)] for j in range(len(zp))]
epsilon = 0.001
n_limit = 1000


def init_random_clusters():
    global clusters
    for i in range(count_clusters):
        new_cluster = random.randint(0, len(zp)-1)
        while new_cluster in clusters:
            new_cluster = random.randint(0, len(zp)-1)
        clusters[i] = new_cluster
    clusters = [zp[i] for i in clusters]


def calc_membership1(x):
    u1 = [0 for i in range(count_clusters)]
    for j in range(count_clusters):
        value_sum = 0
        for k in range(count_clusters):
            numerator = abs(x - clusters[j])
            if numerator == 0:
                u1 = [0 for i1 in range(count_clusters)]
                u1[j] = 1
            else:
                denominator = abs(x - clusters[k])
                if denominator != 0:
                    value_sum += math.pow((numerator/denominator), 3.33)
        if (x != clusters[j] and 1 not in u1):
            value = 1/value_sum
            u1[j] = value
    return u1


def calc_j(mems):
    m = 4
    value = 0
    for i in range(len(zp)):
        for j in range(count_clusters):
            membership = math.pow(mems[i][j], m)
            dist = zp[i] - clusters[j]
            value += membership*dist
    return j


def calc_clusters():
    clusters = [-100 for i in range(count_clusters)]
    m = 1.6
    for j in range(count_clusters):
        numerator = 0
        denominator = 0
        for i in range(len(zp)):
            numerator += math.pow(u[i][j], m)*zp[i]
        for i in range(len(zp)):
            denominator += math.pow(u[i][j], m)
        clusters[j] = numerator/denominator
    return clusters


n = 0
while n < n_limit:
    old_j = calc_j(u)
    clusters = calc_clusters()
    for i in range(len(zp)):
        u[i] = calc_membership1(zp[i])
    new_j = calc_j(u)
    n += 1


labels = [i for i in range(min(zp), max(zp))]
class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        global labels
        return labels


    def get_providers(self):
        return ["Кластер 1", "Кластер 2", "Кластер 3", "Кластер 4"]

    def get_data(self):
        global zp, labels, count_clusters
        data = [0 for i in range(count_clusters)]
        for i in range(count_clusters):
            data[i] = [calc_membership1(i1)[i] for i1 in labels]
        return data


def result(request):
    value_zp = int(request.GET["value_zp"])
    values = calc_membership1(value_zp)
    return render(request, 'lab2/params.html', {"values": values, "zp": value_zp})


line_chart = TemplateView.as_view(template_name='lab2/params.html')
line_chart_json = LineChartJSONView.as_view()

