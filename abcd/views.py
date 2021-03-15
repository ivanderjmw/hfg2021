from django.http.request import HttpRequest
from django.shortcuts import render
# Create your views here.


# Homepage before login
def step1(request: HttpRequest):
    return render(request=request, template_name="abcd/step1.html")

def step2(request: HttpRequest):
    return render(request=request, template_name="abcd/step2.html")

def step3(request: HttpRequest):
    return render(request=request, template_name="abcd/step3.html")

def step4(request: HttpRequest):
    return render(request=request, template_name="abcd/step4.html")

def results(request: HttpRequest):
    return render(request=request, template_name="abcd/finalGraph.html")

def home(request: HttpRequest):
    return render(request=request, template_name="abcd/home.html")
