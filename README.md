# CEA-SIMULATOR

This project is an indoor agriculture simulator that models the relationship of ​crop growth, environment conditions, energy consumptions, and renewable energy generations, and allows a range of operating scenarios simulation for quantitative comparison studies.

## Setup

### Installation

The porject was developed using Django, Pyhton, InfluxDB and MySQL.

> * [Django](https://docs.djangoproject.com/en/3.1/topics/install/)
> * [InfluxDB](https://docs.influxdata.com/influxdb/v1.8/introduction/install/)
> * [MySQL workbench](https://dev.mysql.com/downloads/workbench/)

1. Install Dependencies

> * $ python get-pip.py
> * $ pip install git

2. Clone and Build CEA Simulator

> * $ git clone https://github.com/aaronli-uga/CEA-Simulator.git

   * Libraries required
   
   > * $ pip install pandas
   > * $ pip install numpy
   > * $ pip install pymysql
   > * $ pip install influxdb

### DataBase 

##### InfluxDB

* Install InfluxDB and run it in the terminal/cmd using the following command:

> $ influxd

* Open the influx executable terminal which will appear after the installation. Create a Database and change the database name in task1/maps_app/views.py file and    task1/task1/settings.py files

> **commands**
> * $ create database *dbname*
> * $ use *dbname*

**To load Data into InfluxDB**

1. Open the influxdb folder and open dbinflux.py.
2. Change the database name, api_key and other required attributes.
3. Execute the python file 
> python dbinflux.py

> **Note**
> * The interval can be either 30 minutes or 60 minutes. The years can range from {1998-2018}
> * The max-series limit can be changed in the configuration file as per the user's requirements

##### MySQL

* The MySQL database is primarily used for storing the user's login information

* Open the MySQL workbench and create a local server. Run the mysql server.
* The deafult *auth_user* table can be used or new table can be created. If new table is created change the table name in task1/maps_app/models.py and task1/task1/settings.py files

## Execution

* Open the task1 folder and run the following command:

> python manage.py runserver

* Open the browser and go to

> localhost:8000

   
   

  

