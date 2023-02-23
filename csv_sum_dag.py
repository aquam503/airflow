from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import csv
import datetime
from pathlib import Path


''' 
the owner of the DAG, which is usually the person or
team responsible for maintaining the DAG.
The owner parameter can be useful for organizing and managing 
DAGs in a multi-user environment. For example, it can help to 
identify who is responsible for a particular DAG and provide 
a way for others to contact them if they have questions or issues with the DAG.
'''

default_args = {
    'owner': 'redouane',
    'start_date': datetime.datetime(2023, 2, 22)
}

'''
In Airflow, the name of a DAG is 
the first argument passed to the DAG constructor 
when creating the DAG object.
the name of my DAG is "csv_sum_dag". You can refer to this 
DAG by its name when using Airflow CLI commands (more details = AirflowCLIcommands.txt)
or when defining dependencies between tasks within the DAG.
dag_id===='csv_sum_dag'
By convention, the name of the Python script that defines your DAG should be the same as 
the dag_id parameter that you use when creating the DAG object.
my script name = 'csv_sum_dag.py'
'''

dag = DAG(
    'csv_sum_dag',
    default_args=default_args,
    schedule_interval='*/2 * * * *'
)

def read_csv_and_sum():
    file_name = './data.csv'
    file_path = Path(file_name)

    '''Once you have a Path object representing a file, you can 
    use it to perform various operations on the file, such as opening it 
    for reading or writing, checking whether it exists, and so on.'''

    if file_path.is_file(): #returns true if file exists
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            #reader => every row in a dictionary.
            #reader => [{'Timestamp': '1', 'Value': . },{'Timestamp': '2', 'Value': . },......]
            values = [int(row['Value']) for row in reader]
            total = sum(values)
            print(f'Sum of values: {total}')
            
            # Write sum to CSV file
            with open('./totals.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([datetime.datetime.now(), total])
                #writer.writerow(list for row)
    else:
        print(f'File not found: {file_name}')

csv_sum_operator = PythonOperator(
    task_id='csv_sum_task',
    python_callable=read_csv_and_sum,
    dag=dag
)