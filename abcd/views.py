from abcd.models import *
from abcd.forms import *
from django.http.request import HttpRequest
from django.shortcuts import render
# Create your views here.


# Homepage before login
def step1(request: HttpRequest):
    form = addCommunityForm(request.POST or None)
    if request.method == "POST":
        if not form.is_valid():
            print("invalid")
        else:
            addr = form.cleaned_data['community_addr']
            temp = Community(location=addr)
            temp.save()
    return render(request=request, template_name="abcd/step1.html",
                context={"form": form})

def step2(request: HttpRequest):
    form = addIndividualForm(request.POST or None)
    if request.method == "POST":
        if 'tag_name' in request.POST:
            if not form.is_valid():
                print("invalid")
            else:
                name = form.cleaned_data['individual_name']
                temp = Tags(name=name)
                temp.save()
        else:
            if not form.is_valid():
                print("invalid")
            else:
                name = form.cleaned_data['individual_name']
                temp = Stakeholders(location=name)
                temp.save()
    return render(request=request, template_name="abcd/step2.html",
                  context={"form": form, "tags": {}, "individuals": {}})

def step3(request: HttpRequest):
    form = addAssetForm(request.POST or None)
    if request.method == "POST":
        print(request.user)
        if not form.is_valid():
            print("invalid")
        else:
            name = form.cleaned_data['asset_name']
            temp = Assets(name=name)
            temp.save()
    return render(request=request, template_name="abcd/step3.html")

def step4(request: HttpRequest):
    return render(request=request, template_name="abcd/step4.html")

def results(request: HttpRequest):
    return render(request=request, template_name="abcd/finalGraph.html")

def home(request: HttpRequest):
    return render(request=request, template_name="abcd/home.html")
