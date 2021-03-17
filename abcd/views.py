from datetime import date
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
            temp = Community(name=addr, owner=request.user, location=addr)
            temp.save()
    return render(request=request, template_name="abcd/step1.html",
                context={"form": form})


@login_required(login_url='/login')
def step2(request: HttpRequest):
    form = addIndividualForm(request.POST or None)
    form2 = addTagForm(request.POST or None)
    tags= []
    stakeholders = []
    stakeholders.extend(Stakeholders.objects.all())
    tags.extend(Tags.objects.all())
    print(len(stakeholders))
    print(len(tags))
    if request.method == "POST":
        if 'tag_name' in request.POST:
            if not form2.is_valid():
                print("invalid")
            else:
                name = form2.cleaned_data['tag_name']
                temp = Tags(name=name, owner=request.user)
                temp.save()
        else:
            if not form.is_valid():
                print("invalid")
            else:
                name = form.cleaned_data['individual_name']
                temp = Stakeholders(name=name, owner=request.user)
                temp.save()
    return render(request=request, template_name="abcd/step2.html",
                  context={"form": form, "form2":form2, "tags": tags, "individuals": stakeholders})


@login_required(login_url='/login')
def step3(request: HttpRequest):
    form = addAssetForm(request.POST or None)
    if request.method == "POST":
        print(request.user)
        if not form.is_valid():
            print("invalid")
        else:
            name = form.cleaned_data['asset_name']
            details = form.cleaned_data['asset_details']
            address = form.cleaned_data['asset_address']
            contact = form.cleaned_data['asset_contact']
            temp = Assets(name=name, details=details, address=address, contact=contact, 
                owner=request.user)
            temp.save()
    return render(request=request, template_name="abcd/step3.html")


@login_required(login_url='/login')
def step4(request: HttpRequest):
    return render(request=request, template_name="abcd/step4.html")


@login_required(login_url='/login')
def results(request: HttpRequest):
    json = generateJson(request.user)
    return render(request=request, template_name="abcd/finalGraph.html", context={"data": json})

def home(request: HttpRequest):
    return render(request=request, template_name="abcd/home.html")


def save_graph(request: HttpRequest):
    data = json.loads(request.POST.get('data', ''))
    print(data.__class__)
    d = json.loads(data)
    print(d)
    print(d.__class__)
    nodes = d['nodeDataArray']
    for node in nodes:
        print(node)
        color = node['color']
        x_y = node['loc'].split()
        if color == "yellow": # tags
            target = Tags.objects.get(name=node['key'])
        elif color == "lightblue":  # stakeholder
            print(node['key'])
            target = Stakeholders.objects.get(name=node['key'])
        elif color == "red": # assets
            target = Assets.objects.get(name=node['key'])
        elif color == "blue": # institution
            target = Institutions.objects.get(name=node['key'])
        target.x_coord = x_y[0]
        target.y_coord = x_y[1]
        target.save()
        print(node)
    assocs = d['linkDataArray']
    for assoc in assocs:
        print(assoc)

    return HttpResponse(json.dumps({}),
                    content_type="application/json")


#supporting function
def generateJson(user):
    nodes = []
    nodes.extend(Tags.objects.filter(owner=user))
    nodes.extend(Stakeholders.objects.filter(owner=user))
    nodes.extend(Assets.objects.filter(owner=user))
    nodes.extend(Institutions.objects.filter(owner=user))
    nodes_dic = []
    nodes_dic.extend(map(lambda obj: obj.get_dict(), nodes))
    assocs = []
    d = dict()
    d["class"] = "GraphLinksModel"
    d["linkLabelKeysProperty"] =  "labelKeys"
    d["nodeDataArray"] = nodes_dic
    json_object = json.dumps(d, indent=4)
    return json_object

