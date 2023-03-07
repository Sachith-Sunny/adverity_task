"""
All the initial activities of the project. Extracting Phase and Home page.
"""
import json
import os
import string

import petl as etl
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from transform.views import resolve_homeworld

from .models import File


def name_generator():
    """Custom file name generator"""
    uid = get_random_string(length=10, allowed_chars=string.ascii_letters)
    return str(uid)


def home(request):
    """View for the home page to list all the files"""
    data = File.objects.all()
    return render(request, "home.html", {"data": data})


def show_table(request):
    """Render the final csv file for html template"""
    filename = request.GET.get("fileid", None)
    filename = "./stagefiles/final/" + filename
    table1 = etl.fromcsv(filename)
    table2 = etl.toarray(table1)
    return render(request, "view.html", {"data": table2})


def fetch_api(self):
    """gets the entire data from the api response and stores in the intermediate file."""
    swapi_api = requests.get("https://swapi.dev/api/people?", timeout=20).json()
    results = swapi_api["results"]
    # extending data retrieval to paginated values
    while swapi_api["next"]:
        swapi_api = requests.get(swapi_api["next"], timeout=20).json()
        results.extend(swapi_api["results"])
    json_object = json.dumps(results, indent=4)
    intermediate_stage_1(json_object)
    return home(self)


def intermediate_stage_1(json_object):
    """storing the json response to staging"""
    final_file_name = name_generator()
    file_name = "/stagefiles/intermediate/" + final_file_name + "_stage1.json"
    file_name = os.getcwd() + file_name
    with open(file_name, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    resolve_homeworld(file_name, final_file_name)
    return HttpResponse(json.dumps(json_object), content_type="application/json")


def counter(request):
    """Column combination Counter"""
    filename = request.GET.get("fileid", None)
    filename = "./stagefiles/final/" + filename
    table1 = etl.fromcsv(filename)
    table2 = etl.toarray(table1)
    return render(request, "counter.html", {"data": table2})


@csrf_exempt
def counter_api(request):
    """POST api with 3 parameters : filename,column1,column2"""
    filename = request.GET.get("filename")
    filename = "./stagefiles/final/" + str(filename)
    column1 = request.GET.get("column1", "homeworld")
    column2 = request.GET.get("column2", "birth_year")
    table1 = etl.fromcsv(filename)
    count = etl.valuecounter(table1, column1, column2)
    print(count)
    return HttpResponse(
        json.dumps({"result": "Success"}), content_type="application/json"
    )
