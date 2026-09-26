from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


# Define our task 1
def preprocess_data():
    print("Preprocessing data...")


# Define our task 2
def train_model():
    print("Training Model...")


# Define our task 3
def eval_model():
    print("Evaluating model...")


# Define the DAG
with DAG(
    "ml_pipeline",  # First param is the DAG name
    start_date=datetime(2026, 1, 1),  # Date to start on
    schedule="@weekly",
) as dag:

    # Define the task
    preprocess = PythonOperator(
        task_id="preprocess_task", python_callable=preprocess_data
    )
    train = PythonOperator(task_id="train_task", python_callable=train_model)
    evaluate = PythonOperator(task_id="evaluate_task", python_callable=eval_model)

    # Set dependencies(in which order they should be executed)
    preprocess >> train >> evaluate
