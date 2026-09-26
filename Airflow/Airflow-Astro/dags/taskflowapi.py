from airflow import DAG
from airflow.decorators import task
# from airflow.operators.python import PythonOperator
from datetime import datetime

# define the dag

with DAG(
    dag_id="math_sequence_dag_with_taskapi",
    start_date=datetime(2026,1,1),
    schedule='@once',
    catchup=False
)as dag:
    
    # Task 1 : start with initial number
    @task
    def start_number():
        initial_number = 10
        print(f"starting number: {initial_number}")
        return initial_number # @task needs to return a value
    
    # task 2 : add 5
    @task
    def add_five(number): 
        # number is the context which is the returned value from previous task
        new_value=number + 5
        print(f"add 5: {number}+5={new_value}")
        return new_value
    
    # task 3 : multiply by 2
    @task
    def multiply_by_two(number):
        new_value = number * 2
        print(f"multiply 2: {number}*2={new_value}")
        return new_value
    
    # task 4 : subtract 3
    @task
    def subtract_by_three(number):
        new_value = number - 3
        print(f"Subtract 3: {number}-3={new_value}")
        return new_value
    
    # task 5 : squaring
    @task
    def squaring(number):
        new_value = number ** 2
        print(f"Squaring : {squaring}^2={new_value}")
        return new_value
    
    # Depenedencies
    start_value = start_number()
    added_value = add_five(start_value)
    multiply_value = multiply_by_two(added_value)
    subtracted_value = subtract_by_three(multiply_value)
    square_value = squaring(subtracted_value)