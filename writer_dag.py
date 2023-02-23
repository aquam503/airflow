#this script add a row to a csv file every minute
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pathlib import Path
import csv
import datetime
import time

# set up the file name and header row
file_name = "./data.csv"
header = ["Time", "Value"]

'''write header row to file if file doesn't exist
we want here to check if the file exists or no 
if file exists with open(file_name, "r") as file: will be executed without
error after we use pass : no special action is needed if the CSV file already exists
if the file doesn't exist it will rises FileNotFoundError so
with open(file_name, "w", newline="") will be created '''

'''
The blocks of code outside the function will run only once when you load the DAG file
in Airflow. These blocks define the DAG configuration, set the file name and header
row, define default arguments, and create a DAG object.

The function writer_dag is executed according to the schedule interval defined in
the schedule_interval argument of the DAG object. In this case, the interval is
set to run every minute with '*/1 * * * *'. So, the function will be executed 
once every minute to add a row to the CSV file.
'''

try:
    with open(file_name, "r") as file:
        pass
except FileNotFoundError:
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)

default_args = {
    'owner': 'redouane',
    'start_date': datetime.datetime(2023, 2, 22)
}
dag = DAG(
    'writer_dag',
    default_args=default_args,
    schedule_interval='*/1 * * * *'
)

# open file in append mode
def writer_dag(file_name):
    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)
        while True:
            # get current time and value (in this example, just a random integer)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            value = random.randint(0, 1000)
            # write row to file
            writer.writerow([current_time, value])

# Define the operator that will run the write_to_csv function

'''
you need to pass the complete file path to the op_kwargs dictionary in the 
PythonOperator call, so change 'data.csv' to 'data/data.csv'.
'''

write_csv_op = PythonOperator(
    task_id='write_csv',
    python_callable=writer_dag,
    op_kwargs={'file_name': './data.csv'},
    dag=dag)