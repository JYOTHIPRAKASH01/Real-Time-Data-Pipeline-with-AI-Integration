from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess

def start_kafka_producer():
    subprocess.run(["python", "data_ingestion/kafka_producer.py"])

def start_spark_streaming():
    subprocess.run(["python", "data_processing/spark_streaming.py"])

def start_ai_analysis():
    subprocess.run(["python", "ai_integration/ai_analysis.py"])

# Define the DAG
dag = DAG(
    'real_time_pipeline',
    description='Real-Time Data Pipeline with AI Integration',
    schedule_interval='@hourly',  # Can be adjusted based on your use case
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Define the tasks
task1 = PythonOperator(
    task_id='start_kafka_producer',
    python_callable=start_kafka_producer,
    dag=dag,
)

task2 = PythonOperator(
    task_id='start_spark_streaming',
    python_callable=start_spark_streaming,
    dag=dag,
)

task3 = PythonOperator(
    task_id='start_ai_analysis',
    python_callable=start_ai_analysis,
    dag=dag,
)

# Task dependencies
task1 >> task2 >> task3
