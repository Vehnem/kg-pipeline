import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# st.set_page_config(layout="wide")

if __name__ == '__main__':

    st.title("Data Evaluation")

    st.markdown("---")

    df=pd.DataFrame({
        'Sample': [0, 1, 2],
        'Precision': [0.9, 0.8, 0.7],
        'Recall': [0.9, 0.8, 0.7],
        'F1 Score': [0.9, 0.8, 0.7]
    })

    fig, axes = plt.subplots(3, 1, figsize=(10, 15))

    plt1 = sns.boxplot(data=df, y='Precision', ax=axes[0])
    axes[0].set_title('Precision Scores')
    axes[0].set_xlabel('Sample')

    plt2 = sns.boxplot(data=df, y='Recall', ax=axes[1])
    axes[1].set_title('Recall Scores')
    axes[1].set_xlabel('Sample')

    plt3 = sns.boxplot(data=df, y='F1 Score', ax=axes[2])
    axes[2].set_title('F1 Score Scores')
    axes[2].set_xlabel('Sample')

    con = st.container()
    con.pyplot(plt1.figure, use_container_width=True)

