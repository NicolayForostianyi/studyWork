import math

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django import forms
from django.views.decorators.csrf import csrf_exempt
from model.models import *

this_context = {}

# Create your views here.
def index_error(request, size):
    template = loader.get_template('index.html')
    context = {'size': size}
    return HttpResponse(template.render(context, request))


def index(request):
    if request.method == "GET":
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        size = request.POST.get('size')
        print("||||||||||||||size  = " + str(size))
        return HttpResponseRedirect("build_data/" + str(size))


@csrf_exempt
def build_data(request, size):
    if request.method == "GET":
        print("Размер равен ", size)
        datas = []
        i = 0
        for i in range(int(size)):
            datas.append(Data())
            datas[i].number_of_error = i
            datas[i].index = (i + 1)
        context = {"datas": datas, "size": size}
        template = loader.get_template("build_table.html")
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        print("Метод Post размер равен " + str(size))
        if size is None or int(size) <= 0:
            return HttpResponseRedirect('error/' + str(size))
        else:
            datas = []
            i = 0
            for i in range(int(size)):
                ob = Data()
                num = request.POST.get("number_of_error_" + str(i))
                if num is None or num == "":
                    ob.number_of_error = i
                else:
                    ob.number_of_error = int(num)
                print("ob.number_of_error = ", ob.number_of_error)
                ob.interval = request.POST.get("interval_between_errors_" + str(i))
                print("ob.interval_between_errors_ = ", ob.interval)
                print(ob)
                datas.append(ob)
            B = get_B_of_mininal_difference(datas)
            minimal_difference = get_minimal_difference(datas)
            K = calculate_K(datas, B)
            X_n_plus_1 = calculate_X_n_plus_1(datas, B, K)
            t_k = calculate_t_k(datas, B, K)
            print("Полезная ошибка ", B)
            print("Необходимая разница = ", minimal_difference)
            print("коэффициент пропорциональности K=", K)
            print("среднее время Xn+1 до появления (n+1)-й ошибки = ", X_n_plus_1)
            print(" время до окончания тестирования = ", t_k)
            context ={"B":B}
            context["minimal_difference"]=minimal_difference
            context["K"]=K
            context["X_n_plus_1"]=X_n_plus_1
            context["t_k"]=t_k
            this_context = context
            template = loader.get_template("results.html")
            return HttpResponse(template.render(context, request))


def calculate_t_k(datas, B, K):
    sum_1_del_i = calculate_sum_1_del_i(datas, B)
    result = (1 / K) * sum_1_del_i
    return result


def calculate_sum_1_del_i(datas, B):
    result = float()
    i = 0
    for i in range((B - len(datas))):
        result += 1/(datas[i].number_of_error+1)
    return result


def calculate_X_n_plus_1(datas, B, K):
    return 1/(K * (B - len(datas)))


def calculate_K(datas, B):
    n = len(datas)
    sum_X_i = calculate_sum_Xi(datas)
    sum_iX_i = calculate_sum_i_Xi(datas)
    result = n / ((B + 1) * sum_X_i - sum_iX_i)
    return result


def get_B_of_mininal_difference(datas):
    res = len(datas)
    before_different = float(calculate_F_m(datas, res) - calculate_g_m_A(datas, res))
    next_different = 0.0
    tmp = 0.0
    while True:
        res += 1
        next_different = float(calculate_F_m(datas, res) - calculate_g_m_A(datas, res))
        if math.fabs(before_different) < math.fabs(next_different):
            return res
        before_different = next_different


def get_minimal_difference(datas):
    res = len(datas)
    print("res = ", res)
    before_different = float(calculate_F_m(datas, res) - calculate_g_m_A(datas, res))
    next_different = float()
    tmp = float()
    while True:
        res += 1
        print("Инкремент")
        print("Предыдущая разница = ", before_different)
        next_different = float(calculate_F_m(datas, res) - calculate_g_m_A(datas, res))
        print("Следующая разница", next_different)
        if math.fabs(before_different) < math.fabs(next_different):
            print("Результаты работы программы: предыдущая разница = ", before_different, "следующая разница = ",
                  next_different)
            return float(math.fabs(before_different))
        before_different = next_different


def calculate_F_m(datas, B):
    result = 0
    for dat in datas:
        result += 1 / (B + 1 - dat.number_of_error)
    return result


def calculate_g_m_A(datas, B):
    n = len(datas)
    m = B + 1
    A = calculate_A(datas)
    result = float(n / (m - A))
    return result


def calculate_A(datas):
    sum_i_Xi = calculate_sum_i_Xi(datas)
    sum_Xi = calculate_sum_Xi(datas)
    result = float(sum_i_Xi / sum_Xi)
    return result


def calculate_sum_i_Xi(datas):
    result = 0
    for dat in datas:
        result += float(dat.number_of_error) * float(dat.interval)
    return result


def calculate_sum_Xi(datas):
    result = 0
    for dat in datas:
        result += float(dat.interval)
    return result
