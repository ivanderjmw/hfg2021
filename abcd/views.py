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
    stakeholders.extend(Stakeholders.objects.filter(owner=request.user))
    tags.extend(Tags.objects.filter(owner=request.user))
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

    assets = Assets.objects.filter(owner=request.user)

    return render(request=request, template_name="abcd/step3.html", context={"assets": assets})


@login_required(login_url='/login')
def step4(request: HttpRequest):
    form = addInstitutionForm(request.POST or None)
    if request.method == "POST":
        print(request.user)
        if not form.is_valid():
            print("invalid")
        else:
            name = form.cleaned_data['institution_name']
            details = form.cleaned_data['institution_details']
            address = form.cleaned_data['institution_address']
            contact = form.cleaned_data['institution_contact']
            temp = Institutions(name=name, details=details, address=address, contact=contact, 
                owner=request.user)
            temp.save()

    institutions = Institutions.objects.filter(owner=request.user)
    return render(request=request, template_name="abcd/step4.html", context={"institutions": institutions})

@login_required(login_url='/login')
def step5(request: HttpRequest):
    if request.method == "POST":
        # [{"from": "Alpha", "to": "Beta"}, {"from": "Gamma", "to": "Delta"}]
        # from institutions to stakeholders
        print(request.body)
        print(json.loads(request.body).keys())
        dataDict = json.loads(request.body)

        profile = Profile.objects.get(id=request.user.id)
        assocsString = profile.assocs
        if assocsString == "":
            assocsString = "[]"

        for x in dataDict.keys():
            for y in dataDict[x]:
                assocsString = appendToStringList(
                    assocsString, 
                    createConnString(x, y["name"])
                    )
        profile.assocs = assocsString
        profile.save()


    institutions = Institutions.objects.filter(owner=request.user)
    listInsts = []
    for inst in institutions.iterator():
        listInsts.append(json.dumps({
            "name": inst.name,
            "details": inst.details,
            "address": inst.address,
            "contact": inst.contact
        }))

    stakeholders = Stakeholders.objects.filter(owner=request.user)
    listStakes = []
    
    for stake in stakeholders.iterator():
        listStakes.append(json.dumps({
            "name": stake.name
        }))

    dataDict = {"institutions": listInsts, "stakeholders": listStakes}
    data = json.dumps(dataDict)
    return render(request=request, template_name="abcd/step5.html", context={"data": data})

@login_required(login_url='/login')
def results(request: HttpRequest):
    json = generateJson(request.user)
    return render(request=request, template_name="abcd/finalGraph.html", context={"data": json})

def home(request: HttpRequest):
    return render(request=request, template_name="abcd/home.html")


def save_graph(request: HttpRequest):
    data = json.loads(request.POST.get('data', ''))
    d = json.loads(data)
    print(d)
    nodes = d['nodeDataArray']
    for node in nodes:
        color = node['color']
        x_y = node['loc'].split()
        if color == "yellow": # tags
            target = Tags.objects.filter(owner=request.user).get(name=node['key'])
        elif color == "lightblue":  # stakeholder
            target = Stakeholders.objects.filter(owner=request.user).get(name=node['key'])
        elif color == "red": # assets
            target = Assets.objects.filter(owner=request.user).get(name=node['key'])
        elif color == "blue": # institution
            target = Institutions.objects.filter(owner=request.user).get(name=node['key'])
        target.x_coord = x_y[0]
        target.y_coord = x_y[1]
        target.save()
    assocs = d['linkDataArray']
    profile = Profile.objects.get(id=request.user.id)
    profile.assocs = json.dumps(assocs)
    profile.save()


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
    if (not user.assocs == ""):
        data = json.loads(user.assocs)
        print(data)
        assocs = data
    d = dict()
    d["class"] = "GraphLinksModel"
    d["linkLabelKeysProperty"] =  "labelKeys"
    d["nodeDataArray"] = nodes_dic
    d["linkDataArray"] = assocs
    json_object = json.dumps(d, indent=4)
    return json_object

def createConnString(fromItem, toItem):
    connString = "{"
    connString += "from:" + "\"" + fromItem + "\""
    connString += ","
    connString += "to:" + "\"" + toItem + "\""
    connString += "}"
    return connString

def appendToStringList(stringList, item):
    if stringList == "[]":
        return "[" + item + "]"

    if stringList.find(item) >= 0:
        return stringList
    return stringList[:-1] + "," + item + "]"
