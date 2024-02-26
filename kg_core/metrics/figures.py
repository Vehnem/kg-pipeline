import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
def plot_precision_recall_f1(scores) -> plt:
    """
    Generate precision, recall, and f1-score boxplots using seaborn based on a list of scores.
    
    Args:
    - scores (list of tuples): A list where each tuple contains (precision, recall, f1_score).
    """
    # Unpack scores into separate lists
    precision_scores, recall_scores, f1_scores = zip(*scores)
    
    # Prepare data for boxplot
    data = {
        'Precision': precision_scores,
        'Recall': recall_scores,
        'F1 Score': f1_scores
    }
    df = pd.DataFrame(data)
    
    # Create a figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    
    # Plot precision scores boxplot
    sns.boxplot(data=df, y='Precision', ax=axes[0])
    axes[0].set_title('Precision Scores')
    axes[0].set_xlabel('Sample')
    
    # Plot recall scores boxplot
    sns.boxplot(data=df, y='Recall', ax=axes[1])
    axes[1].set_title('Recall Scores')
    axes[1].set_xlabel('Sample')
    
    # Plot F1 scores boxplot
    sns.boxplot(data=df, y='F1 Score', ax=axes[2])
    axes[2].set_title('F1 Scores')
    axes[2].set_xlabel('Sample')
    
    # Adjust layout
    plt.tight_layout()
    
    plt.savefig('boxplot.png')
    # Display the plot

# Example usage:
scores = [
    (0,0,0),
    (0.9, 0.8, 0.85),
    (0.92, 0.82, 0.87),
    (0.88, 0.78, 0.82),
    # ... more scores
]
p = plot_precision_recall_f1(scores)
