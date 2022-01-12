# Statistics collector

### Description

This API will help you with storing advertising statistics for your applications, ads, etc.

You can save parameters such as ***сost***, ***views***, ***clicks*** by dates. 
***Api automatically summarizes statistics for the day*** and ***calculates CPM (Cost per Mille) and CPC (Cost per click).***

### Tech
 - [Django REST Framework] - toolkit for building Web APIs
 - [PostgreSQL] - open source object-relational database

### Instalation

First:
```sh
git clone https://github.com/M11N3/StatisticsCollector
```
Go to the directory and create **.env** file with following values:
```sh
cd StatisticsCollector/
touch .env
```


**.env file**:
```env
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
SECRET_KEY=
```

Add up docker images:
```sh
docker-compose up --build --no-deps
```

### Methods
+ #### `<GET> http://localhost:8000/statistic/`
   This method displays all stored statistics for all the time.
    **query_params**:
    ```
         date_from:     DateField("YYYY-MM_DD")      (Optional)
         date_to:       DateField("YYYY-MM_DD")      (Optional)
         ordering: Str(<name_ordering_field>)   (Optional)
    ```
    
    To display statistics for a time interval use the parameters __?from__ (start date) AND __?to__ (end date):
    The __from__ and __to__ dates are included in the selection.
    `http://localhost:8000/statistic/?from=<date>&to=<date>`
    
    To sort in ascending order using:
   `http://localhost:8000/statistic/?ordering=<field_name>` 
    If you want to sort in descending order, then use "-" symbol before the field name:
   `http://localhost:8000/statistic/?ordering=-<field_name>` 
   
     **ordering fields**:
    |field name|description|
    |----------|--|
    |cost      |the amount of money spent per day|
    |date      |date                             |
    |clicks    |total number of clicks per day   |
    |views     |total number of views per day    |
    |cpc       |cost per click                   |
    |cpm       |cost per mille                   |
    
    The response is automatically calculated cost per mille (CPM) and cost per click (CPC).
    ***response***:
    ```json
    [{
        "date": ...,
        "cost": ...,
        "clicks": ...,
        "views": ...,
        "cpc": ...,
        "cpm": ...
     }]
    ```

* #### `<POST> http://localhost:8000/statistic/`

    To save statistics send a post request with the following fields.
    
    ***Fields:***
    |Field name | description | required |
    |-----------|---------------------------------|----------|
    |date | This DateField format YYYY-MM-DD| + |
    |cost | PostiveIntegerField | - |
    |views | PostiveIntegerField | - |
    |clicks | PostiveIntegerField | - |
    
    If you save statistic in fist time for this date:
    ```sh
    curl -d '{"date":"2022-01-01", "cost":"100", "clicks":"100", "views":"100"}' -H "Content-Type: application/json" -X POST http://localhost:8000/statistic/
    ```
    
    You will receive the following **response**:
    `status: 201 Created`
    **data**:
    ```json
    [{
        "date": "2022-01-01",
        "cost": "100.00",
        "clicks": 100,
        "views": 100
    }]
    ```
    
    When you send request with statistic on existing date then api updates instance with summation of fields(cost, views, clicks).
    ----------------------------------------------------------------------------
    ____________________________________________________________________________________________________________________
    
    **Example:**
    API has following data:
    ```json
    [{
        "date": "2022-01-01",
        "cost": "100.00",
        "clicks": 100,
        "views": 100,
        "cpc": 1,
        "cpm": 1000
    }]
    ```
    
    If you send the following request:
    ```sh
    curl -d '{"date":"2022-01-01", "cost":"100", "clicks":"100", "views":"100"}' -H "Content-Type: application/json" -X POST http://localhost:8000/statistic/
    ```
    
    You will receive the following **response**:
    `status: 201 Created`
    **data**:
    ```json
    [{
        "date": "2022-01-01",
        "cost": "200.00",
        "clicks": 200,
        "views": 200
    }]
    ```
    
    ### If you send `invalid data values` you get folliwing ***response***:
    `status: 400 Bad Request`
    **data**:
    ```json
    {
        "field name": [
            "error_message"
        ]
    }
    ```

+ #### `<DELETE> http://localhost:8000/statistic/`
    ###### `WARNING:`  This method `delete all statistic`.

    ***response***:
    ```
    status: 204 No Content
    ```

[Django REST Framework]:https://www.django-rest-framework.org/
[PostgreSQL]: https://www.postgresql.org/
