from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator

# from kgflex.kgflex import MyCustomOperator, MyCustomOperator2

import json
import os

class BaseOperator(BaseOperator):
    def execute(self, context):
        with open("result_of"+self.task_id+".out", "a") as f:
            f.write(f"DummyOperator {self.task_id} executed\n")
        return

# 1) Define where to find your DAG config file
CONFIG_PATH = "dags/dag_config.json"

# 2) Load the config at parse time
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

nodes = config["nodes"]
edges = config["edges"]

# 3) Create a DAG
dag = DAG(
    dag_id="my_dynamic_dag",
    start_date=days_ago(1),
    schedule_interval="@daily"
)

# 4) Create an Airflow operator for each node
#    You could customize the operator type if you stored that info in the config.
operators = {}
for node in nodes:
    operators[node] = BaseOperator(
        task_id=node,
        dag=dag
    )

# 5) Set dependencies based on edges
for (upstream, downstream) in edges:
    operators[upstream] >> operators[downstream]

# 6) Register the DAG so Airflow sees it
globals()["my_dynamic_dag"] = dag



    # docker_task1 = DockerOperator(
    #     docker_url='tcp://docker-proxy:2375',
    #     task_id='docker_task1',
    #     image="python:3.8",
    #     command="python -c 'print(\"Hello from Docker!\")'",
    # )


    # docker_task1 >>docker_task

