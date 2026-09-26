"""
We'll define a DAG where the tasks are as follows:

Task 1: Start with an initial tiber (e.g., 10).
Task 2: Add 5 to the number.
Task 3: Multiply the result by 2.
Task 4: Subtract 3 from the result.
Task 5: Compute the square of the result.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define funciton for each task


# Context is used to give context to next tasks
def start_number(**context):
    # xcom_push is the way to pass the context
    context["ti"].xcom_push(key="current_value", value=10)
    print("Starting number 10")


def add_five(**context):
    current_val = context["ti"].xcom_pull(key="current_value", task_ids="start_task")
    new_value = current_val + 5
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"add 5: {current_val}+5={new_value}")


def multiply_by_two(**context):
    current_val = context["ti"].xcom_pull(
        key="current_value", task_ids="add_five_task"
    )
    new_value = current_val * 2
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"multiply 2: {current_val}*2={new_value}")


def subtract_by_three(**context):
    current_val = context["ti"].xcom_pull(
        key="current_value", task_ids="multiply_by_two_task"
    )
    new_value = current_val - 3
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"Subtract 3: {current_val}-3={new_value}")


def squaring(**context):
    current_val = context["ti"].xcom_pull(
        key="current_value",
        task_ids="subtract_by_three_task",
        # task_ids-> previous task related name to know from which task it is pulling the value
    )
    new_value = current_val**2
    context["ti"].xcom_push(key="current_value", value=new_value)
    print(f"Squaring : {current_val}^2={new_value}")


# Define the DAG
with DAG(
    dag_id="math_sequence_dag",
    start_date=datetime(2026, 1, 1),
    schedule="@once",
    catchup=False,
) as dag:

    # Define the task
    start_task = PythonOperator(
        task_id="start_task", # Should be same name as given above in task_ids
        python_callable=start_number, 
        # provide_context=True --> Depricated
    )
    
    add_five_task= PythonOperator(
        task_id="add_five_task",
        python_callable=add_five, 
        # provide_context=True
    )
    
    multiply_by_two_task= PythonOperator(
        task_id="multiply_by_two_task",
        python_callable=multiply_by_two, 
        #provide_context=True
        )
    
    subtract_by_three_task= PythonOperator(
            task_id="subtract_by_three_task",
            python_callable=subtract_by_three, 
            #provide_context=True
            )

    squaring_task= PythonOperator(
                task_id="squaring_task",
                python_callable=squaring, 
                #provide_context=True
                )

    # Dependencies
    start_task >> add_five_task >> multiply_by_two_task >> subtract_by_three_task >> squaring_task