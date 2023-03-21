# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago
###############################################
###############################################
#defining DAG arguments
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Redouane',
    'start_date': days_ago(0),
    'email': ['redouane@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
###############################################
###############################################
# defining the DAG

# define the DAG

dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)


unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -zxvf /home/project/tolldata.tgz -C /home/project/airflow/dags/finalassignment',
    dag=dag,
)

extract_data_from_csv = BashOperator(
    task_id='extract_csv',
    bash_command='cut -f1,2,3,4 -d"," /home/project/airflow/dags/finalassignment/vehicle-data.csv > /home/project/airflow/dags/csv_data.csv',
    dag=dag,
)


extract_data_from_tsv = BashOperator(
    task_id='extract_tsv',
    bash_command="cut -f5,6,7 -d $'\t' /home/project/airflow/dags/finalassignment/tollplaza-data.tsv > /home/project/airflow/dags/tsv_data.csv",
    dag=dag,
)


extract_data_from_fixed_width = BashOperator(
    task_id='extract_txt',
    bash_command='cut -c 59-67 /home/project/airflow/dags/finalassignment/payment-data.txt > /home/project/airflow/dags/fixed_width_data.csv',
    dag=dag,
)


consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste  /home/project/airflow/dags/csv_data.csv  /home/project/airflow/dags/tsv_data.csv  /home/project/airflow/dags/fixed_width_data.csv  >  /home/project/airflow/dags/extracted_data.csv',
    dag=dag,
)

#This task should transform the vehicle_type field in extracted_data.csv 
#into capital letters and save it into a 
#file named transformed_data.csv in the staging directory.
#tr '[:lower:]' '[:upper:]' < input.txt > output.txt
transform_data = BashOperator(
task_id='transform_data',
bash_command="tr '[:lower:]' '[:upper:]' < /home/project/airflow/dags/extracted_data.csv | cut -d',' -f4 | cut -f1 -d $'\t' > /home/project/airflow/dags/finalassignment/staging/transformed_data.csv",
dag=dag,
)


# task pipeline

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data