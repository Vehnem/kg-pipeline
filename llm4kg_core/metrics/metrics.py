#Evaluation metrics for the LLM4KG project

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

class Metrics:
    """
    Metrics to calulate the performance of the model
    - Accuracy
    - Precision
    - Recall
    - F1-score
    """

    def accuracy(self, y_true, y_pred):
        """
        Calculates the accuracy of the model
        """
        return accuracy_score(y_true, y_pred)
    

    def precision(self, y_true, y_pred):
        """
        Calculates the precision of the model
        """
        return precision_score(y_true, y_pred)
