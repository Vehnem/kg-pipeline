#Evaluation metrics for the LLM4KG project

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from rdflib import Graph

# todo https://networkx.org/documentation/stable/reference/algorithms/similarity.html

class Metrics:
    """
    Metrics to calulate the performance of the model
    - Accuracy
    - Precision
    - Recall
    - F1-score
    """

    def accuracy_score(self, y_true, y_pred):
        """
        Calculates the accuracy of the model

        How close a measurement or attempt is to the actual value or target

        """
        return accuracy_score(y_true, y_pred)
    

    def precision_score(self, y_true, y_pred):
        """
        Calculates the precision of the model
        How consistent the results are regardless of proximity to the actual value or target
        This is not needed for the LLM4KG project
        """
        return precision_score(y_true, y_pred)
    

    def recall_score(self, y_true, y_pred):
        """
        Calculates the recall of the model
        """
        return recall_score(y_true, y_pred)
    

    def f1_score(self, y_true, y_pred):
        """
        Calculates the f1-score of the model
        """
        return f1_score(y_true, y_pred)
    

class RDF_Similarity_Metrics:
    """
    Metrics to calulate the RDF similarity of the model
    """
    pass

    def __init__(self, g1: Graph, g2: Graph) -> None:
        self.g1 = g1
        self.g2 = g2
        pass


    def precision_score(self):
        pass

    def recall_score(self):
        pass

    def f1_score(self):
        pass