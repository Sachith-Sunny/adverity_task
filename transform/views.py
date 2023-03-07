import datetime
import json
import re

import petl as etl
import requests

from load.views import save_file


def resolve_homeworld(filename, final_file_name):
    """homeworld field is changed to its name"""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        for i in data:
            fetched_data = requests.get(i["homeworld"], timeout=20).json()
            i["homeworld"] = fetched_data["name"]
    file_name = "./stagefiles/intermediate/" + final_file_name + "_stage2.json"
    with open(file_name, "w", encoding="utf-8") as out:
        json.dump(data, out, indent=4)
    remove_unwanted_fields(file_name, final_file_name)


def remove_unwanted_fields(file_name, final_file_name):
    """Stripping of unnecessary fields"""
    table1 = etl.fromjson(file_name)
    table1 = etl.cutout(
        table1, "films", "species", "vehicles", "starships", "created", "url"
    )
    file_name = "./stagefiles/intermediate/" + final_file_name + "_stage3.csv"
    etl.tocsv(table1, file_name)
    date_change(file_name, final_file_name)


def date_formatter(value, row):
    """Date formating to YMD. value argument is required for etl convert pass_row = True"""
    date = re.search("\d{4}-\d{2}-\d{2}", row.date)
    new_date = datetime.datetime.strptime(date.group(), "%Y-%m-%d").date()
    return str(new_date)


def date_change(file_name, final_file_name):
    """Changing column header to date"""
    table1 = etl.fromcsv(file_name)
    table1 = etl.rename(table1, "edited", "date")
    table1 = etl.convert(table1, "date", date_formatter, pass_row=True)
    file_name = "./stagefiles/intermediate/" + final_file_name + "_stage4.csv"
    etl.tocsv(table1, file_name)
    save_file(file_name, final_file_name)
