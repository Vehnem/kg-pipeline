from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator

# from kgflex.kgflex import MyCustomOperator, MyCustomOperator2
from kgflex_tools.tasks import *

import json
import os

with DAG(
    dag_id='test_tools_paris',
    schedule_interval=None,
    catchup=False,
    tags=['kg_integration', "test"]
) as dag:
    ErMatchingOperator(task_id='er_matching_with_paris', input="some.ttl")
