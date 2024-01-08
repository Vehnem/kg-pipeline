###Prompts for ontology mapping task###

class RMLPrompts:

    def __init__(self) -> None:
        pass

    def prompt0(self, ontology_ser, data_ser): """
    Genearte an RML mapping in the turtle format for the following ontology and data source.

    ### Ontology: 
    {ontology_ser}

    ### CSV Data:
    {data_ser} 
    """