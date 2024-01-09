#Evaluation metrics for the LLM4KG project

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

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
    

# # Example data
# true_labels = [0, 1, 1, 0, 1]
# predicted_labels = [0, 1, 0, 0, 1]

# # Calculate accuracy
# accuracy = accuracy_score(true_labels, predicted_labels)

# # Calculate recall
# recall = recall_score(true_labels, predicted_labels)

# # Calculate F1 score
# f1 = f1_score(true_labels, predicted_labels)

# print("Accuracy:", accuracy)
# print("Recall:", recall)
# print("F1 Score:", f1)