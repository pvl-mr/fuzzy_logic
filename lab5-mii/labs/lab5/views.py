from chartjs.colors import next_color
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

triangle_parameters = []
trapez_parameters = []

data = []
count_dots = 75
clear_time_series = [[-2.5,
            -5,
            -5,
            -5.5,
            -7.5,
            -4.5,
            0,
            0.5,
            -2,
            0.5,
            -2,
            0.5,
            -0.5,
            -3,
            -2,
            -1.5,
            -0,5,
            -1,
            1.5,
            1,
            1,
            0.5,
            -0.5,
            2,
            -0.5,
            -0.5,
            0,
            0.5,
            -1,
            -0.5,
            2.5,
            0,
            0,
            -1.5,
            -2,
            -2,
            0,
            -4,
            -7,
            -5.5,
            -1,
            -1,
            0.5,
            1.5,
            0,
            -2,
            -1.5,
            1,
            1,
            4,
            5,
            6,
            4,
            2,
            2,
            4.5,
            -3,
            -1.5,
            0,
            -0.5,
            0,
            1,
            0.5,
            0,
            1,
            2,
            2,
            2.5,
            9.5,
            7.5,
            6.5,
            3,
            9]]
fuzzy_data = []
triangle_parameters = [[-8, -6, -4], [-6, -4, -2], [-4, -2, 0], [-2, 0, 2], [0, 2, 4], [2, 4, 6], [4, 6, 8], [6, 8, 10]]
trapez_parameters = []
predicted_values = [0 for i in range(len(clear_time_series))]
high = [None for i in range(count_dots)]
low = [None for i in range(count_dots)]

class LineChartJSONView3(BaseLineChartView):
    def get_labels(self):
        global count_dots
        return [i for i in range(10)]

    def get_providers(self):
        global triangle_parameters, trapez_parameters
        return [f"Функция {i}" for i in range(1, len(triangle_parameters)+len(trapez_parameters))]

    def get_data(self):
        global data
        return data


class LineChartJSONClearView(BaseLineChartView):
    def get_labels(self):
        return [i for i in range(count_dots)]

    def get_providers(self):
        # return ['Чёткий временной ряд']
        return ['Чёткий временной ряд', 'Прогнозируемые значения']

    def get_data(self):
        global clear_time_series, predicted_values
        # data = clear_time_series.append(predicted_values)
        # print(f"normal data 2 {data}")
        print(f"predicted values {predicted_values}")
        # return clear_time_series
        return [clear_time_series[0], predicted_values]

def generateArraysData():
    result = []
    clear_time_series_copy = clear_time_series[0]
    for i in range(1, len(clear_time_series_copy)):
        if (clear_time_series_copy[i - 1] >= clear_time_series_copy[i]):
            result

class LineChartJSONFuzzyView(BaseLineChartView):
    def get_labels(self):
        global count_dots
        return [i for i in range(count_dots)]

    def get_providers(self):
        global triangle_parameters, trapez_parameters
        # return ["Функция", 'Прогнозируемые значения']
        return ['Функция']

    def get_data(self):
        global fuzzy_data, predicted_values
        # return [fuzzy_data[0], predicted_values[0]]
        return fuzzy_data


def index(request):
    return render(request, 'lab3/params.html', {'result': ""})


def triangle_mem_func(x, requestData):
    a = requestData[0]
    b = requestData[1]
    c = requestData[2]
    if a <= x <= b:
        return (x-a)/(b-a)
    elif b <= x <= c:
        return (c-x)/(c-b)
    elif x < a or x > c:
        return 0

def trapez_mem_func(x, requestData):
    a = requestData[0]
    b = requestData[1]
    c = requestData[2]
    d = requestData[3]
    if a <= x <= b:
        return 1 - (b - x) / (b - a)
    elif b <= x <= c:
        return 1
    elif c <= x <= d:
        return 1 - (x - c) / (d - c)
    else:
        return 0

def prepare_data(pars):
    global triangle_parameters, trapez_parameters
    triangle_parameters = []
    trapez_parameters = []
    for i in range(len(pars)):
        item = pars.getlist(f'triangle_parameters[{i}]', '')
        if item != '':
            triangle_parameters.append([int(k) for k in item])
    for i in range(len(pars)):
        item = pars.getlist(f'trapez_parameters[{i}]', '')
        if item != '':
            trapez_parameters.append([int(k) for k in item])

def prepare_result(pars=[], status=0):
    # status - 0 - no additional params
    # status 1 - additional params
    global triangle_parameters, trapez_parameters, data, count_dots
    if status != 0:
        prepare_data(pars)
    data = []
    for pars in triangle_parameters:
        data.append([triangle_mem_func(i, pars) for i in range(count_dots)])
    for pars in trapez_parameters:
        data.append([trapez_mem_func(i, pars) for i in range(count_dots)])



line_chart4 = TemplateView.as_view(template_name='lab5/index.html')
line_chart_clear_time_series = TemplateView.as_view(template_name='lab5/index.html')
line_chart_fuzzy_time_series = TemplateView.as_view(template_name='lab5/index.html')

line_chart_json5 = LineChartJSONView3.as_view()
line_chart_json_clear_time_series = LineChartJSONClearView.as_view()
line_chart_json_fuzzy_time_series = LineChartJSONFuzzyView.as_view()

def calc_fuzzy_times():
    global fuzzy_data, clear_time_series
    fuzzy_data = [0]
    for i in range(len(clear_time_series[0])):
        fuzzy_data.append(calc_one_series(i))
    fuzzy_data = [fuzzy_data]
    return fuzzy_data

def calc_one_series(i):
    global fuzzy_data, clear_time_series, trapez_parameters, triangle_parameters
    triangles_values = []
    trapez_values = []
    triangles_values += [triangle_mem_func(clear_time_series[0][i], triangle_parameter) for triangle_parameter in triangle_parameters]
    trapez_values += [trapez_mem_func(clear_time_series[0][i], trapez_parameter) for trapez_parameter in trapez_parameters]
    max_value = max(triangles_values)
    fun_i = triangles_values.index(max_value)+1
    return fun_i

def lab5(request):
    global triangle_parameters, trapez_parameters
    prepare_result()
    calc_fuzzy_times()
    predict(fazificate(triangle_parameters))
    return render(request, 'lab5/index.html')


# def predict_values():
#     global fuzzy_data, predicted_values
#     predicted_values[0] = fuzzy_data[0]
#     for i in range(len(fuzzy_data)-1):
#         prev_fuzzy_value = fuzzy_data[i-1]
#         prev_index = 0
#         func_value = fuzzy_data.index(prev_fuzzy_value, prev_index)
#         predicted_values[i] =


def predict(a):
    global predicted_values
    table_a = []
    conclusion = [[] for i in range(len(triangle_parameters)+1)]
    for i in range(len(a) - 1):
        table_a.append([a[i], a[i + 1]])
    for i in range(len(triangle_parameters)+1):
        for j in range(len(table_a)):
            if table_a[j][0] == i:
                conclusion[i].append(table_a[j][1])
    conclusion_2 = []
    for i in conclusion:
        value = 0
        for j in i:
            value += triangle_parameters[j][1]
        if len(i) != 0:
            value = value / len(i)
        conclusion_2.append(value)
    predicted_values = [0 for i in range(len(a))]
    predicted_values[0] = a[0]
    for i in range(1, len(a)):
        predicted_values[i] = conclusion_2[a[i]]

def fazificate(triangle_parameters):
    a = []
    time_series = clear_time_series[0]
    for item in time_series:
        values = [triangle_mem_func(item, triangle_parameter) for triangle_parameter in triangle_parameters]
        a.append(values.index(max(values)))
    return a