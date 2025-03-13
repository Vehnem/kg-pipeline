import networkx as nx
from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.dates import days_ago

class MyCustomOperator(BaseOperator):
    @apply_defaults
    def __init__(self, my_param: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_param = my_param

    def execute(self, context):
        self.log.info(f"Executing MyCustomOperator with param: {self.my_param}")

# Find the shortest path based on edge weights
task_graph = nx.DiGraph()

# Define a directed graph where nodes are tasks and edges are dependencies

# Example tasks with input and output file formats
task_graph.add_edge("extract_csv", "transform_json", weight=1)  # extract_csv -> transform_json
task_graph.add_edge("transform_json", "load_db", weight=1)       # transform_json -> load_db
task_graph.add_edge("extract_csv", "validate_csv", weight=2)     # Alternative path
task_graph.add_edge("validate_csv", "load_db", weight=2)         # Alternative path

start_task = "extract_csv"
end_task = "load_db"

shortest_path = nx.shortest_path(task_graph, source=start_task, target=end_task, weight="weight")
print("Shortest path:", shortest_path)

def create_task(task_id, dag):
    """Helper function to create a Dummy task"""
    return MyCustomOperator(task_id=task_id, dag=dag, my_param="Hello Airflow")

def create_dag_from_graph(dag_id, graph, start_node, end_node):
    dag = DAG(dag_id, tags="kg_integration")

    # Compute the shortest path
    path = nx.shortest_path(graph, source=start_node, target=end_node, weight="weight")
    print(f"Using path: {path}")

    # Create tasks dynamically
    tasks = {task: create_task(task, dag) for task in path}

    # Set dependencies along the path
    for i in range(len(path) - 1):
        tasks[path[i]] >> tasks[path[i + 1]]

    return dag

# Generate the DAG dynamically
dag_id = "dynamic_dag"
dag = create_dag_from_graph(dag_id, task_graph, "extract_csv", "load_db")

# Register DAG globally for Airflow to pick up
globals()[dag_id] = dag

print("DONE ")