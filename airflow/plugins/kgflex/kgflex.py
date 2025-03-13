from airflow.plugins_manager import AirflowPlugin
from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook
from airflow.utils.decorators import apply_defaults
from airflow.providers.docker.operators.docker import DockerOperator
from typing import Any

# # Custom Operator
# class MyCustomOperator(BaseOperator):
#     @apply_defaults
#     def __init__(self, conn_id: str, query: str, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.conn_id = conn_id
#         self.query = query

#     def execute(self, context):
#         self.log.info("Executing custom operator")
#         hook = MyCustomHook(self.conn_id)
#         result = hook.run_query(self.query)
#         self.log.info(f"Query Result: {result}")
#         return result


# # Custom Operator
# class MyCustomOperator2(BaseOperator):
#     @apply_defaults
#     def __init__(self, conn_id: str, query: str, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.conn_id = conn_id
#         self.query = query

#     def execute(self, context):
#         self.log.info("Executing custom operator")
#         hook = MyCustomHook(self.conn_id)
#         result = hook.run_query(self.query)
#         self.log.info(f"Query Result: {result}")
#         return result
