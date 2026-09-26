from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.utils.dates import days_ago --> depricated
from datetime import datetime
import json

with DAG(
    dag_id="NASA_apod_postgres",
    start_date = datetime(2026,1,1),
    schedule="@daily",
    catchup=False
)as dag:
    
    # Step 1: Create the table if it does not exists
    @task
    def create_table():
        # initialize the postgreshook --> to interact with postgres
        # postgres_conn_id --> id we are providing for postgres connection
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")

        # SQl query to create the table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );

        """
        
        # Execute the table creating query
        postgres_hook.run(create_table_query)
    
    # Step 2: Extract NASA api data(APOD - Astronomy Picture of the Day)[Extract] 
    extract_apod = HttpOperator(
        task_id = "extract_apod",
        http_conn_id="nasa_api", # conn id defined in airflow for nasa api
        endpoint="planetary/apod", # nasa api endpoint for apod
        method="GET",
        data={"api_key":"{{ conn.nasa_api.extra_dejson.api_key }}"}, # use the api key from the conn
        response_filter= lambda response: response.json() # convert response to json
    )
    
    # Step 3: Tranform the data( pick the information that i need to save)
    @task
    def transform_apod_data(response):
        apod_data={
            # reponse.get(required_title, show this if not found(which is blank here))
            'title': response.get('title',''),
            'explanation': response.get('explanation',''),
            'url': response.get('url',''),
            'date': response.get('date',''),
            'media_type': response.get('media_type','')
        }
        return apod_data
    
    # Step 4: Loading data into postgres sql
    @task
    def load_data_to_postgres(apod_data):
        # initialize the postgres hook
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")

        # define SQL insert query
        insert_query="""
        INSERT INTO apod_data (title, explanation,url,date,media_type)
        VALUES(%s,%s,%s,%s,%s);
        """
        
        # Execute the SQL query
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))

    # Step 5: verify the data using DBeaver
    # i used postgres client extension to verify in vs code itself
    
    
    # Step 6: define the task dependencies
    
    # extract part
    create_table() >> extract_apod #Ensure table is created before execution
    api_response = extract_apod.output
    
    # Transform part
    transform_data=transform_apod_data(api_response)
    
    # Load part
    load_data_to_postgres(transform_data)