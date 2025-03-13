###Hierachy###

import networkx as nx

proc_graph = nx.DiGraph()

proc_graph.add_node("Information_Extraction", type="process")
proc_graph.add_node("Data_Cleaning", type="process")
proc_graph.add_node("Entity_Resolution", type="process")

proc_graph.add_node("NER", type="subprocess")
proc_graph.add_node("NEL", type="subprocess")
proc_graph.add_node("REL", type="subprocess")
proc_graph.add_edges_from([
    ("Information_Extraction", "NER"),
    ("Information_Extraction", "NEL"),
    ("Information_Extraction", "REL")
])

proc_graph.add_node("Magellan_ER", type="subprocess")
proc_graph.add_edge("Entity_Resolution", "Magellan_ER")

proc_graph.add_node("Magellan_ER_Implementation", type="task")
proc_graph.add_edge("Magellan_ER", "Magellan_ER_Implementation")

print("Process Hierarchy:", list(proc_graph.edges))


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
