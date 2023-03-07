SETUP :

Setup virtual environment and install packages 
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Setup and configure a postgresql database based on the settings_.py file with the credentials as in the file


Running the server : 

Once DB is setup, run the following commands to start the development server:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Usage :
```
http://127.0.0.1:8000/home/
```

This will give you the list of files in the filesystem and a ```
fetch```  button to retrieve the latest results from swapi .

Clicking the ```
fetch ``` button starts the retreival of data from swapi.
On success a new row entry can be seen in the table with timestamp.

Clicking on a row entry will display the transformed data in the file.
[ ```Go to Counter``` link not implemented fully.]

API to get the count of occurences of column values
```
http://127.0.0.1:8000/api/counter?filename=EEDWVlSvdq.csv&column1=eye_color&column2=birth_year
```
will print the results of the count in the terminal.
where ``` filename, column1, column2 ``` can be supplied with name of file and column names to be combined to make the count, respectively.


![screenshot_api](https://user-images.githubusercontent.com/26067833/223445157-3afde27d-2588-493d-ad61-8025031dc013.png)


#Code structure

api - does the initial extraction and views for html pages

transform - does the data transformation

load - saves the final file and adds metadata to model

templates - html files

stagefiles

  intermediate - files stored after each transformation as ```filename_stage_number```
    
  final - files stored in ```filename.csv``` format.
 

#TODO

1) Count functionality is now implemented as API. Write Javascript functions and change the views accordingly to implement the functionality as per the requirements.
2) Exception handling for requests and files
4) Write tests for the functions with pytest and pytest-cov to check the coverage.
5) Setup lint and formating with pylint, black, isort etc
6) CI/CD for deployment.

