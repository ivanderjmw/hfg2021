import json
from django.contrib.auth.decorators import login_required
from abcd.models import *
from abcd.forms import *
from django.http.request import HttpRequest
from django.shortcuts import render
# Create your views here.


# Homepage before login
@login_required(login_url='/login')
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


@login_required(login_url='/login')
def step2(request: HttpRequest):
    form = addIndividualForm(request.POST or None)
    initial_data = {"class": "GraphLinksModel",
            "linkLabelKeysProperty": "labelKeys",
            "nodeDataArray": [
                {"key": "Alpha", "color": "lightblue", "loc": "29 14"},
                {"key": "Beta", "color": "orange", "loc": "145 -5"},
                {"key": "Gamma", "color": "lightgreen", "loc": "29 106"},
                {"key": "Delta", "color": "pink", "loc": "129 106"}
            ],
            "linkDataArray": [
                {"from": "Alpha", "to": "Beta",
                 "labelKeys": ["A-B"]},
                {"from": "Gamma", "to": "Delta",
                 "labelKeys": ["G-D"]},
                {"from": "Alpha", "to": "Gamma",
                 "labelKeys": ["A-G"]},
                {"from": "Beta", "to": "Gamma",
                 "labelKeys": [-8], "category":""},
                {"from": "Beta", "to": "Delta", "labelKeys": [-5]},
                {"from": "Alpha", "to": "Delta", "labelKeys": [-6]}
            ]}
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
                data = {"class": "GraphLinksModel",
                        "linkLabelKeysProperty": "labelKeys",
                        "nodeDataArray": [
                            {"key": "Alpha", "color": "lightblue", "loc": "29 14"},
                            {"key": "Beta", "color": "orange", "loc": "145 -5"},
                            {"key": "Gamma", "color": "lightgreen", "loc": "29 106"},
                            {"key": "Delta", "color": "pink", "loc": "129 106"}
                        ],
                        "linkDataArray": [
                            {"from": "Alpha", "to": "Beta",
                                "labelKeys": ["A-B"]},
                            {"from": "Gamma", "to": "Delta",
                                "labelKeys": ["G-D"]},
                            {"from": "Alpha", "to": "Gamma",
                                "labelKeys": ["A-G"]},
                            {"from": "Beta", "to": "Gamma",
                                "labelKeys": [-8], "category":""},
                            {"from": "Beta", "to": "Delta", "labelKeys": [-5]},
                            {"from": "Alpha", "to": "Delta", "labelKeys": [-6]}
                        ]}
                temp = Stakeholders(name=name, x_coord=4)
                print("DONE")
                temp.save()
                print(Stakeholders)
    return render(request=request, template_name="abcd/step2.html",
                  context={"form": form, "tags": {}, "individuals": {}, "data": initial_data})


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def step4(request: HttpRequest):
    return render(request=request, template_name="abcd/step4.html")


@login_required(login_url='/login')
def results(request: HttpRequest):
    return render(request=request, template_name="abcd/finalGraph.html")

def home(request: HttpRequest):
    return render(request=request, template_name="abcd/home.html")

#supporting function
def generateJson():
    nodes =[]
    assocs = []
    # Profile.objects.all[0].assocs
    dict = {
        "class": "GraphLinksModel",
        "linkLabelKeysProperty": "labelKeys",
        "nodeDataArray": nodes,
        "linkDataArray": assocs
    }

