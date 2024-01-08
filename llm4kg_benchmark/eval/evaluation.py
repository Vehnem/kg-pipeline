import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerTuple
import pandas as pd

# Assuming you have the data for accuracy, recall, and f1 score

# 
# 

# accuracy_data = [0.85, 0.92, 0.88, 0.90, 0.87]
# recall_data = [0.80, 0.85, 0.82, 0.88, 0.84]
# f1_score_data = [0.82, 0.88, 0.85, 0.86, 0.83]

# expected triples = 11

gpt3_a = [0/10, 4/6, 4/6, 4/7, 0/10]
gpt3i_a = [0/10, 4/6, 4/6, 4/4, 4/6]
gpt4_a = [10/10, 4/4, 4/6, 4/6, 4/4]

gpt3_r = [0/10, 4/10, 4/10, 4/10, 0/10]
gpt3i_r = [0/10, 4/10, 4/10, 4/10, 4/10]
gpt4_r = [10/10, 4/10, 4/10, 4/10, 4/10]

def calculate_f1_score(accuracy, recall):
    precision = accuracy
    if((precision+recall) == 0):
        return 0
    else:
        return 2 * ((precision * recall) / (precision + recall))

gpt3_f1 = []
for accuracy, recall in zip(gpt3_a, gpt3_r):
    f1_score = calculate_f1_score(accuracy, recall)
    gpt3_f1.append(f1_score)

gpt3i_f1 = []
for accuracy, recall in zip(gpt3i_a, gpt3i_r):
    f1_score = calculate_f1_score(accuracy, recall)
    gpt3i_f1.append(f1_score)

gpt4_f1 = []
for accuracy, recall in zip(gpt4_a, gpt4_r):
    f1_score = calculate_f1_score(accuracy, recall)
    gpt4_f1.append(f1_score)

print(gpt3_f1)
print(gpt3i_f1)
print(gpt4_f1)

# gpt3_f1 = [0, 0.88, 0.85, 0.86, 0.83]
# gpt3i_f1 = [0.82, 0.88, 0.85, 0.86, 0.83]
# gpt4_f1 = [0.82, 0.88, 0.85, 0.86, 0.83]

# Create a dataframe with the data
data_a = {'GPT-3': gpt3_a, 'GPT-3-Inst.': gpt3i_a, 'GPT-4': gpt4_a}
data_r = {'GPT-3': gpt3_r, 'GPT-3-Inst.': gpt3i_r, 'GPT-4': gpt4_r}
data_f1 = {'GPT-3': gpt3_f1, 'GPT-3-Inst.': gpt3i_f1, 'GPT-4': gpt4_f1}

# data = {'Accuracy': accuracy_data, 'Recall': recall_data, 'F1 Score': f1_score_data}

df_a = pd.DataFrame(data_a)
df_r = pd.DataFrame(data_r)
df_f1 = pd.DataFrame(data_r)

# Create the boxplot using seaborn
sns.boxplot(data=df_a, orient='v')

# Set the labels and title
plt.xlabel('Model')
plt.ylabel('Score')
plt.title('Accuracy')

# Show the plot
plt.savefig("a.png")

# Create the boxplot using seaborn
sns.boxplot(data=df_r, orient='v')

# Set the labels and title
plt.xlabel('Model')
plt.ylabel('Score')
plt.title('Recall')

# Show the plot
plt.savefig("r.png")

# Create the boxplot using seaborn
sns.boxplot(data=df_f1, orient='v')

# Set the labels and title
plt.xlabel('Model')
plt.ylabel('Score')
plt.title('F1')

# Show the plot
plt.savefig("f1.png")

def avg(arr):
    return sum(arr) / len(arr)

print("GPT3",avg(gpt3_a), avg(gpt3_r), avg(gpt3_f1))
print("GPT3i",avg(gpt3i_a), avg(gpt3i_r), avg(gpt3i_f1))
print("GPT4",avg(gpt4_a), avg(gpt4_r), avg(gpt4_f1))