from chartjs.colors import next_color
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

triangle_parameters = []
trapez_parameters = []
data = []
count_dots = 20
clear_time_series = [[1, 3, 5, 4, 2, 7, 2, 7, 9, 15, 7, 14, 10, 5, 13, 2, 7, 7, 11, 8]]
fuzzy_data = []
triangle_parameters = [[1, 2, 4], [13, 5, 7], [6, 8, 9], [8, 11, 13], [12, 14, 15]]
trapez_parameters = []
high = [None for i in range(count_dots)]
low = [None for i in range(count_dots)]

class LineChartJSONView3(BaseLineChartView):
    def get_labels(self):
        global count_dots
        return [i for i in range(count_dots)]

    def get_providers(self):
        global triangle_parameters, trapez_parameters
        return [f"Функция {i}" for i in range(1, len(triangle_parameters)+len(trapez_parameters)+1)]

    def get_data(self):
        global data
        return data


class LineChartJSONClearView(BaseLineChartView):
    def get_colors(self):
        color_list = (
            (13, 118, 94), (13, 118, 94), (13, 118, 94), (13, 118, 94), (13, 118, 94), (13, 118, 94), (13, 118, 94),
            (199, 15, 34),

            (202, 201, 197),  # Light gray,

            (122, 159, 191),  # Light blue
            )
        return next_color(color_list)

    def get_labels(self):
        return [i for i in range(count_dots)]

    def get_providers(self):
        return ['Чёткий временной ряд']

    def get_data(self):
        # global high, low
        global clear_time_series
        print(f"sample of clear is {clear_time_series}")
        return clear_time_series
        # return [high, low]


def get_high():
    global high
    print(f"count dots is {count_dots}")
    for i in range(count_dots - 1):
        if clear_time_series[0][i] < clear_time_series[0][i+1]:
            print(f"clear[i] i = {i}, value =  {clear_time_series[0][i]}")
            print(f"clear[i+1] i = {i+1}, value =  {clear_time_series[0][i+1]}")
            high[i] = clear_time_series[0][i]
    print(f"high is {high}")
    return high


def get_low():
    global low
    for i in range(count_dots - 1):
        if clear_time_series[0][i] > clear_time_series[0][i+1]:
            print(f"clear[i] i = {i}, value =  {clear_time_series[0][i]}")
            print(f"clear[i+1] i = {i+1}, value =  {clear_time_series[0][i+1]}")
            low[i] = clear_time_series[0][i]
    print(f"high is {low}")
    return low


def generateArraysData():
    result = []
    tempResult = []
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
        return [f"Нечёткий временной ряд"]

    def get_data(self):
        global fuzzy_data
        return fuzzy_data

class LineChartJSONTendenciesView(BaseLineChartView):
    def get_colors(self):
        color_list = (
            (13, 118, 94),
            (199, 15, 34),
            )
        return next_color(color_list)
    def get_labels(self):
        global count_dots
        return [i for i in range(count_dots)]

    def get_providers(self):
        global triangle_parameters, trapez_parameters
        return [f"Тендеция верх", "Тенденция вниз"]

    def get_data(self):
        # global fuzzy_data
        global high, low
        return [high, low]


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


def lab3_result(request):
    pars = request.GET
    prepare_result(pars, 1)
    return render(request, 'lab3/graphic.html')

def lab3_params(request):
    return render(request, 'lab3/params.html')

line_chart4 = TemplateView.as_view(template_name='lab4/index.html')
line_chart_clear_time_series = TemplateView.as_view(template_name='lab4/index.html')
line_chart_fuzzy_time_series = TemplateView.as_view(template_name='lab4/index.html')
line_chart_json_tendencies = TemplateView.as_view(template_name='lab4/index.html')

line_chart_json4 = LineChartJSONView3.as_view()
line_chart_json_clear_time_series = LineChartJSONClearView.as_view()
line_chart_json_fuzzy_time_series = LineChartJSONFuzzyView.as_view()
line_chart_json_tendencies = LineChartJSONTendenciesView.as_view()

def calc_fuzzy_times():
    global fuzzy_data, clear_time_series
    fuzzy_data = [0]
    for i in range(len(clear_time_series[0])):
        fuzzy_data.append(calc_one_series(i))
    print(f"fuzzy data is {fuzzy_data}")
    fuzzy_data = [fuzzy_data]
    return fuzzy_data

def calc_one_series(i):
    global fuzzy_data, clear_time_series, trapez_parameters, triangle_parameters
    triangles_values = []
    trapez_values = []
    triangles_values += [triangle_mem_func(clear_time_series[0][i], triangle_parameter) for triangle_parameter in triangle_parameters]
    trapez_values += [trapez_mem_func(clear_time_series[0][i], trapez_parameter) for trapez_parameter in trapez_parameters]
    # return max(max(triangles_values), max(trapez_values))
    max_value = max(triangles_values)
    fun_i = triangles_values.index(max_value)+1
    return fun_i

def lab4(request):
    global triangle_parameters, trapez_parameters
    prepare_result()
    # calc_one_series(1)
    calc_fuzzy_times()
    get_high()
    get_low()
    return render(request, 'lab4/index.html')



