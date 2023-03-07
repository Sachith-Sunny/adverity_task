import petl as etl

from api.models import File


def save_file(file_name, final_file_name):
    """Final saving of transformed Data"""
    table1 = etl.fromcsv(file_name)
    file_name = "./stagefiles/final/" + final_file_name + ".csv"
    etl.tocsv(table1, file_name)
    final_file_name = final_file_name + ".csv"
    File.objects.create(name=str(final_file_name))
