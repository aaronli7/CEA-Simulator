# CEA-SIMULATOR

This project is an indoor agriculture simulator that models the relationship of ​crop growth, environment conditions, energy consumptions, and renewable energy generations, and allows a range of operating scenarios simulation for quantitative comparison studies.

## Setup

### Technologies Used
* Front-end: HTML, CSS, JavaScript, AJAX
*	Back-end: Python (Django)
*	Databases: InfluxDB, MySQL


### Installation

The porject was developed using Django, Pyhton, InfluxDB and MySQL.

> * [Django](https://docs.djangoproject.com/en/3.1/topics/install/)
> * [InfluxDB](https://docs.influxdata.com/influxdb/v1.8/introduction/install/)
> * [MySQL workbench](https://dev.mysql.com/downloads/workbench/)

1. Install Dependencies

>  $ python get-pip.py</br>
>  $ pip install git

2. Clone and Build CEA Simulator

>  $ git clone https://github.com/aaronli-uga/CEA-Simulator.git

   * Libraries required
   
   >  $ pip install pandas</br>
   >  $ pip install numpy</br>
   >  $ pip install mysqlclient</br>
   >  $ pip install pymysql</br>
   >  $ pip install Ipython</br>
   >  $ pip install influxdb

### DataBase 

##### InfluxDB

* Install InfluxDB and run it in the terminal/cmd using the following command:

> $ influxd

* Open the influx executable terminal which will appear after the installation. Create a Database and change the database name in task1/maps_app/views.py file and    task1/task1/settings.py files

> **commands**
>  $ create database *dbname* </br>
>  $ use *dbname*

**To load Data into InfluxDB**

1. Open the influxdb folder and open dbinflux.py.
2. Change the database name, api_key and other required attributes.
3. Execute the python file 
> $ python dbinflux.py

> **Note**
> * The interval can be either 30 minutes or 60 minutes. The years can range from {1998-2018}
> * The max-series limit can be changed in the configuration file as per the user's requirements

##### MySQL

* The MySQL database is primarily used for storing the user's login information

* Open the MySQL workbench and create a local server. Run the mysql server.
* The deafult *auth_user* table can be used or new table can be created. If new table is created change the table name in task1/maps_app/models.py and task1/task1/settings.py files

### Folder Structure & File Descriptions

1. **influxdb/**
    * dbinflux.py - This is used to pull the data from NREL website by using the API
    * final1.csv - Latitude and Longitude information for all locations in USA

2. **task1/**
    * maps_app/
        * models.py - contains the MySQL db table information
        * sim.py & simulator.py - it executes the simulation
        * urls.py - contains the path to the views
        * views.py - contains all the backend code
    * static/ - contains the webpage designs in css/ , fonts/, js/ and the images in images/ 
    * task1/
        * settings.py - OS Path, static file and database configurations
    * templates/maps_app - it contains the webpages
        * chart.html - chart is being displayed by Google’s Visualization API
        * index.html - first page of the website
        * mainpage.html - home page of the website (after user logged in)
        * mappage.html - page where user is being asked for input
        * table1.html & table2.html - table view of the graph that is being displayed


## Execution

* Open the task1 folder and run the following command:

> $ python manage.py runserver

* Open the browser and go to

> localhost:8000

### WorkFlow

1. User creates an account or logs in to the existing account.
2. Parameters such as temperature, CO2, date, and location are selected by the user.
3. These parameters are passed to the Crop Growth Simulator and three CSV files (username_distri.csv, username_fruitdev.csv, username_growth.csv) are generated.
4. The CSV files are stored in influxDB
5. The data is being passed as an input to the Google Visualization API.
6. The output from the Google Visualization API is the graph that is being displayed.
7. Responsive table is also being generated using the data


   
   

  

