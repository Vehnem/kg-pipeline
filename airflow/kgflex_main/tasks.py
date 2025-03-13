import networkx as nx

# Initialize a directed graph for process hierarchy
process_tree = nx.DiGraph()

# High-Level Processes
process_tree.add_node("Information_Extraction", type="process")
process_tree.add_node("Data_Cleaning", type="process")
process_tree.add_node("Entity_Resolution", type="process")

# Sub-Processes for Information Extraction
process_tree.add_node("NER", type="subprocess")
process_tree.add_node("NEL", type="subprocess")
process_tree.add_node("REL", type="subprocess")
process_tree.add_edges_from([
    ("Information_Extraction", "NER"),
    ("Information_Extraction", "NEL"),
    ("Information_Extraction", "REL")
])

# Sub-Process for Entity Resolution
process_tree.add_node("Magellan_ER", type="subprocess")
process_tree.add_edge("Entity_Resolution", "Magellan_ER")

# Implementations (Tasks)
process_tree.add_node("Magellan_ER_Implementation", type="task")
process_tree.add_edge("Magellan_ER", "Magellan_ER_Implementation")

# Visualize the structure
print("Process Hierarchy:", list(process_tree.edges))

# Define exchange formats for each process
process_io = {
    "Information_Extraction": {"input": ["TEXT"], "output": ["EXTRACTED_DATA"]},
    "Entity_Resolution": {"input": ["EXTRACTED_DATA"], "output": ["MATCHED_ENTITIES"]},
    "Magellan_ER": {"input": ["EXTRACTED_DATA"], "output": ["MATCHED_ENTITIES"]},
    "Magellan_ER_Implementation": {"input": ["EXTRACTED_DATA"], "output": ["MATCHED_ENTITIES"]},
}

# Define available conversions
conversion_map = {
    ("TEXT", "EXTRACTED_DATA"): "TextToExtractedData",
    ("EXTRACTED_DATA", "MATCHED_ENTITIES"): "ExtractedDataToMatchedEntities"
}

def get_required_conversions(input_format, required_format):
    """
    Returns a conversion task if needed.
    """
    if (input_format, required_format) in conversion_map:
        return conversion_map[(input_format, required_format)]
    return None  # No conversion needed


def find_execution_path(start_data, end_data):
    """
    Finds the valid execution path from input to output format.
    Ensures required conversions are included.
    """
    path = []
    current_data = start_data

    # Traverse process hierarchy
    for process in nx.topological_sort(process_tree):
        if process in process_io:
            required_input = process_io[process]["input"][0]
            required_output = process_io[process]["output"][0]

            # If input format doesn't match, add conversion step
            if required_input != current_data:
                conversion_task = get_required_conversions(current_data, required_input)
                if conversion_task:
                    path.append(conversion_task)
                    current_data = required_input  # Update format after conversion

            # Add the process itself
            path.append(process)
            current_data = required_output  # Update format

            # Stop when reaching the final format
            if current_data == end_data:
                break

    return path

# Example: Find path from TEXT to MATCHED_ENTITIES
execution_path = find_execution_path("TEXT", "MATCHED_ENTITIES")
print("Execution Path:", execution_path)
