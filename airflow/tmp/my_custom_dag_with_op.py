from airflow import DAG
from airflow.utils.dates import days_ago
from my_custom_operator import MyCustomOperator

with DAG("my_custom_dag_with_operator", schedule_interval=None, tags=["kg_integration"]) as dag:
    MyCustomOperator(task_id="my_task", my_param="Hello Airflow")
