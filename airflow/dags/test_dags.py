from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator
# from kgflex.kgflex import MyCustomOperator, MyCustomOperator2
from kgflex_tools.tasks import *

with DAG(
    dag_id='test_echo_docker',
    schedule_interval=None,
    catchup=False,
    tags=['kg_integration', "test"]
) as dag:
    DockerOperator(
        docker_url='tcp://docker-proxy:2375',
        task_id='echo_cat',
        image="python:3.8",
        mounts=[
            {
            "target": "/share",
            "source": "/workspace/data/kgflex/share",
            "type": "bind"
            }
        ],
        command="bash -c 'ls -a /share >> /share/ls.out'",
    )

with DAG(
    dag_id='test_date_bash',
    schedule_interval=None,
    catchup=False,
    tags=['kg_integration', "test"]
) as dag:
    BashOperator(
        task_id='print_date',
        bash_command='date',
    )

# with DAG(
#     dag_id='test_custom_operator',
#     schedule_interval=None,
#     catchup=False,
#     tags=['kg_integration', "test"]
# ) as dag:
#     task1 = MyCustomOperator(task_id='my_task', conn_id="test_conn", query="SELECT 1")
#     task2 = MyCustomOperator2(task_id='my_task2',  conn_id="test_conn", query="SELECT 1")

#     task1 >> task2


# with DAG(
#     dag_id='test_tools_paris2',
#     schedule_interval=None,
#     catchup=False,
#     tags=['kg_integration', "test"]
# ) as dag:
#     ER_MATCHING_WITH_PARIS
