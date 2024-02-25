from llm4kg_core.metrics.metrics import Metrics

def test_metrics():
    metrics = Metrics()
    # Example data
    true_labels = [0, 1, 1, 0, 1]
    predicted_labels = [0, 1, 0, 0, 1]

    # Calculate accuracy
    accuracy = metrics.accuracy_score(true_labels, predicted_labels)

    # Calculate recall
    recall = metrics.recall_score(true_labels, predicted_labels)

    # Calculate F1 score
    f1 = metrics.f1_score(true_labels, predicted_labels)

    print("Accuracy:", accuracy)
    print("Recall:", recall)
    print("F1 Score:", f1)

def test_metrics_2():
    pass