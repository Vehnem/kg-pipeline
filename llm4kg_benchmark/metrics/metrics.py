from sklearn.metrics import accuracy_score, recall_score, f1_score

# Example data
true_labels = [0, 1, 1, 0, 1]
predicted_labels = [0, 1, 0, 0, 1]

# Calculate accuracy
accuracy = accuracy_score(true_labels, predicted_labels)

# Calculate recall
recall = recall_score(true_labels, predicted_labels)

# Calculate F1 score
f1 = f1_score(true_labels, predicted_labels)

print("Accuracy:", accuracy)
print("Recall:", recall)
print("F1 Score:", f1)

