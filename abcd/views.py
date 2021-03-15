from django.http.request import HttpRequest
from django.shortcuts import render
# Create your views here.


# Homepage before login
def landing(request: HttpRequest):
    return render(request=request, template_name="abcd/landing.html")

def home(request: HttpRequest):
    return render(request=request, template_name="abcd/home.html")