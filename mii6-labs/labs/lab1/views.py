from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

requestData_russia, requestData_france = [0, 0, 0], [0, 0, 0]

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return [i for i in range(20)]

    def get_providers(self):
        return ["Функция принадлежности России", "Функция принадлежности Франции"]

    def get_data(self):
        """Return 3 datasets to plot."""
        global requestData_russia
        global requestData_france

        return [requestData_russia, requestData_france]


line_chart = TemplateView.as_view(template_name='lab1/params.html')
line_chart_json = LineChartJSONView.as_view()

def index(request):
    return render(request, 'lab1/params.html', {'result': ""})


def trapez_mem_func(x, requestData):
    a = requestData[0]
    b = requestData[1]
    c = requestData[2]
    if a <= x <= b:
        return (x-a)/(b-a)
    elif b <= x <= c:
        return (c-x)/(c-b)
    elif x < a or x > c:
        return 0



def result(request):
    temp = float(request.GET["temp"])
    global requestData_russia
    global requestData_france
    requestData_russia = [float(request.GET["a"]), float(request.GET["b"]), float(request.GET["c"])]
    requestData_france = [float(request.GET["a2"]), float(request.GET["b2"]), float(request.GET["c2"])]
    print("requestData_russia", requestData_russia)
    temp_russia, temp_france = trapez_mem_func(temp, requestData_russia), trapez_mem_func(temp, requestData_france)
    requestDataParams_russia, requestDataParams_france = requestData_russia, requestData_france
    requestData_russia = [trapez_mem_func(i, requestDataParams_russia) for i in range(20)]
    requestData_france = [trapez_mem_func(i, requestDataParams_france) for i in range(20)]
    return render(request, 'lab1/params.html', {'res_russia': temp_russia, "res_france": temp_france, "par1": temp,
                                                "pars": requestDataParams_russia, "pars2": requestDataParams_france, "temp": temp
                                                })



