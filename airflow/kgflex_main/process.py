# Parent process: Cleaning
cleaning_io = {
    "Cleaning": {
        "input": ["RAW"],
        "output": ["CLEANED_DATA"]
    }
}

# Sub-processes
cleaning_subprocesses_io = {
    "Error_Detection": {
        "input": ["RAW"],
        "output": ["ERROR_REPORT"]
    },
    "Error_Removal": {
        "input": ["RAW", "ERROR_REPORT"],
        "output": ["CLEANED_DATA"]
    }
}

# Concrete tasks (implementations)
cleaning_tasks_io = {
    "Error_Detection_with_CustomImpl": {
        "input": ["RAW"],
        "output": ["ERROR_REPORT"]
    },
    "Error_Removal_with_MyTool": {
        "input": ["RAW", "ERROR_REPORT"],
        "output": ["CLEANED_DATA"]
    }
}

# Parent process: Extraction
extraction_io = {
    "Extraction": {
        "input": ["CLEANED_DATA"],
        "output": ["EXTRACTED_DATA"]
    }
}

# Sub-processes
extraction_subprocesses_io = {
    "NER": {
        "input": ["CLEANED_DATA"],
        "output": ["ANNOTATED_DATA"]
    },
    "NEL": {
        "input": ["ANNOTATED_DATA"],
        "output": ["EXTRACTED_DATA"]
    }
}

# Concrete tasks (implementations)
extraction_tasks_io = {
    "NER_with_CoreNLP": {
        "input": ["CLEANED_DATA"],
        "output": ["ANNOTATED_DATA"]
    },
    "NER_with_DBpedia_Spotlight": {
        "input": ["CLEANED_DATA"],
        "output": ["ANNOTATED_DATA"]
    },
    "NEL_with_Foo": {
        "input": ["ANNOTATED_DATA"],
        "output": ["EXTRACTED_DATA"]
    },
    "REL_with_Bar": {
        "input": ["ANNOTATED_DATA"],
        "output": ["EXTRACTED_DATA"]
    }
}

# Parent process: EntityResolution
er_io = {
    "EntityResolution": {
        "input": ["EXTRACTED_DATA"],
        "output": ["MATCH_RESULTS"] 
    }
}

# Sub-processes
er_subprocesses_io = {
    "Blocking": {
        "input": ["EXTRACTED_DATA"],
        "output": ["CANDIDATE_PAIRS"]
    },
    "Matching": {
        "input": ["CANDIDATE_PAIRS"],
        "output": ["MATCHED_ENTITIES"]
    },
    "Fusion": {
        "input": ["MATCHED_ENTITIES"],
        "output": ["MATCH_RESULTS"]
    }
}

# Concrete tasks (implementations)
er_tasks_io = {
    "Blocking_with_TechX": {
        "input": ["EXTRACTED_DATA"],
        "output": ["CANDIDATE_PAIRS"]
    },
    "Matching_with_Paris": {
        "input": ["CANDIDATE_PAIRS"],
        "output": ["MATCHED_ENTITIES"]
    },
    "Fusion_with_SomeTool": {
        "input": ["MATCHED_ENTITIES"],
        "output": ["MATCH_RESULTS"]
    }
}

import networkx as nx

hierarchy = nx.DiGraph()

# 1) Parent (abstract) processes as nodes
hierarchy.add_node("Cleaning", type="abstract_process", **cleaning_io["Cleaning"])
hierarchy.add_node("Extraction", type="abstract_process", **extraction_io["Extraction"])
hierarchy.add_node("EntityResolution", type="abstract_process", **er_io["EntityResolution"])

# 2) Sub-processes for each parent
def add_subprocesses(parent, subprocesses_io):
    for subproc, io_def in subprocesses_io.items():
        hierarchy.add_node(subproc, type="subprocess", **io_def)
        hierarchy.add_edge(parent, subproc)  # link parent -> sub-process

add_subprocesses("Cleaning", cleaning_subprocesses_io)
add_subprocesses("Extraction", extraction_subprocesses_io)
add_subprocesses("EntityResolution", er_subprocesses_io)

# 3) Concrete tasks
def add_implementations(subprocesses_io, tasks_io):
    """
    For each sub-process, link its possible implementations (tasks).
    """
    for subproc in subprocesses_io:
        # The subproc has input X and output Y
        for task_name, task_io in tasks_io.items():
            # If the task matches the subproc's IO, we can link subproc -> task
            if (task_io["input"] == subprocesses_io[subproc]["input"] and
                task_io["output"] == subprocesses_io[subproc]["output"]):
                hierarchy.add_node(task_name, type="task", **task_io)
                hierarchy.add_edge(subproc, task_name)

add_implementations(cleaning_subprocesses_io, cleaning_tasks_io)
add_implementations(extraction_subprocesses_io, extraction_tasks_io)
add_implementations(er_subprocesses_io, er_tasks_io)

# Inspect
print("Edges in the hierarchy:")
for u,v in hierarchy.edges:
    print(f"  {u} -> {v}")

def build_pipeline(hierarchy, pipeline_stages):
    """
    pipeline_stages = [
      ("Cleaning", "Error_Detection_with_CustomImpl", "Error_Removal_with_MyTool"),
      ("Extraction", "NER_with_CoreNLP", "NEL_with_Foo"),
      ("EntityResolution", "Blocking_with_TechX", "Matching_with_Paris", "Fusion_with_SomeTool")
    ]
    """
    selected_nodes = []
    for stage_tuple in pipeline_stages:
        parent_process = stage_tuple[0]
        # The rest are chosen sub-process tasks
        tasks = stage_tuple[1:]
        selected_nodes.append(parent_process)
        for t in tasks:
            selected_nodes.append(t)
    return selected_nodes

pipeline_stages = [
    ("Cleaning", "Error_Detection_with_CustomImpl", "Error_Removal_with_MyTool"),
    ("Extraction", "NER_with_CoreNLP", "NEL_with_Foo"),
    ("EntityResolution", "Blocking_with_TechX", "Matching_with_Paris", "Fusion_with_SomeTool")
]

# This yields an ordered list of the processes + tasks that we want to run
execution_order = build_pipeline(hierarchy, pipeline_stages)
print("Execution order:", execution_order)

import networkx as nx
import json

def build_config():
    # 1) Create a directed graph
    G = nx.DiGraph()

    # 2) Add nodes (tasks) & edges (dependencies)
    #    This is an illustrative example.
    G.add_node("Cleaning")
    G.add_node("Error_Detection_with_CustomImpl")
    G.add_node("Error_Removal_with_MyTool")
    G.add_edge("Cleaning", "Error_Detection_with_CustomImpl")
    G.add_edge("Error_Detection_with_CustomImpl", "Error_Removal_with_MyTool")

    # 3) Convert the graph into a data structure we can store:
    #    For instance, just store the node list & edge list.
    nodes = list(G.nodes)
    edges = list(G.edges)

    config = {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "description": "A sample DAG from RAW to CLEANED_DATA"
        }
    }
    return config

if __name__ == "__main__":
    config_data = build_config()
    with open("dag_config.json", "w") as f:
        json.dump(config_data, f, indent=2)


# from airflow import DAG
# from airflow.operators import BaseOperator
# from airflow.utils.dates import days_ago

# class DummyOperator(BaseOperator):
#     def execute(self, context):
#         with open("result_of"+self.task_id+".out", "a") as f:
#             f.write(f"DummyOperator {self.task_id} executed\n")
#         return

# def create_airflow_dag(dag_id, node_list):
#     dag = DAG(dag_id, start_date=days_ago(1), schedule_interval="@daily")

#     ops = {}
#     for node in node_list:
#         node_type = hierarchy.nodes[node]["type"]
#         # If it's a "task", create a real Airflow operator. If it's abstract, maybe just skip or create a DummyOperator
#         if node_type in ["task", "subprocess", "abstract_process"]:
#             ops[node] = DummyOperator(task_id=node, dag=dag)
#         else:
#             # Or handle differently
#             ops[node] = DummyOperator(task_id=node, dag=dag)

#     # Link them in linear order for simplicity:
#     for i in range(len(node_list) - 1):
#         ops[node_list[i]] >> ops[node_list[i+1]]

#     return dag

# dag_id = "complete_data_pipeline"
# dag = create_airflow_dag(dag_id, execution_order)
# globals()[dag_id] = dag
