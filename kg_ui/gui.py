import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import random
from io import BytesIO


# def plot_figure():
#     fig, ax = plt.subplots()
#     ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
#     return fig

st.title("Hello World!")
st.header("This is a header")
st.subheader("This is a subheader")
st.write("This is some text.")

# df = pd.DataFrame([
#     {'modelId': 'gpt4', 'score_name': 'no_repair', 'score_value': 2},
#     {'modelId': 'gpt4', 'score_name': 'one_reapir', 'score_value': 2},
#     {'modelId': 'gpt4', 'score_name': 'two_repair', 'score_value': 4},
#     {'modelId': 'gpt4', 'score_name': 'more_than_two_repair', 'score_value': 2},
#     {'modelId': 'gpt3', 'score_name': 'no_repair', 'score_value': 1},
#     {'modelId': 'gpt3', 'score_name': 'one_reapir', 'score_value': 3},
#     {'modelId': 'gpt3', 'score_name': 'two_repair', 'score_value': 2},
#     {'modelId': 'gpt3', 'score_name': 'more_than_two_repair', 'score_value': 4},
# ])

pal = plt.cm.tab20c
st.write(pal(0))

# https://stackoverflow.com/questions/73568416/create-a-stacked-bar-plot-and-annotate-with-count-and-percent

dic = {
    '0 repair attempts needed':      [3,  38, 35, 16, 12],
    '1 repair attempt needed':       [6,  0,  3,  18,  4],
    '2 repair attempts needed':      [3,  1,  0,  0,  0],
    'not repaired after 2 attempts': [28, 1,  2,  6,  24],
}

df = pd.DataFrame(dic, index=['claude2.1','claude3-opus', 'gpt3.5', 'gpt4', 'gemini-pro'], columns=list(dic.keys()))
st.write(df)

# plot dataframe
plot = df.plot(kind='bar', stacked=True, color=[pal(8), pal(0), pal(1), pal(4)])
plot.set_ylabel('#Runs')
buf = BytesIO()
plt.tight_layout()
plot.get_figure().savefig(buf, format="png")
st.image(buf)

# {
#   "gemini-pro": {
#     "cnt": 13,
#     "error_code_not_0": 12,
#     "error_code_0_empty_output": 1
#   },
#   "claude-3-opus-20240229": {
#     "cnt": 39,
#     "error_code_0_empty_output": 11,
#     "valid_turtle": 23,
#     "not_valid_turtle": 5
#   },
#   "gpt-3.5-turbo": {
#     "cnt": 38,
#     "error_code_not_0": 38
#   },
#   "gpt-4": {
#     "cnt": 18,
#     "error_code_0_empty_output": 4, # emtpy
#     "error_code_not_0": 4, # rml_exception
#     "valid_turtle": 7, # valid_turtle
#     "not_valid_turtle": 3 # rdf4j_exception
#   }
# }

df = pd.DataFrame({
    'generates triples':   [0, 26, 0,  13, 0],
    'zero triples':        [4, 8,  2,  6, 1],
    # 'rdf4j_exception':   [0, 4,  2,  12, 0],
    # 'rml_exception':     [8, 1,  34, 3, 15],
    'rmlmapper exception': [8, 5,  38, 15, 13],
}, index=['claude2.1','claude3-opus', 'gpt3.5', 'gpt4', 'gemini-pro'], columns=['generates triples', 'zero triples', 'rmlmapper exception'])
st.write(df)

# plot dataframe
plot = df.plot(kind='bar', stacked=True, color=[pal(0), pal(17), pal(4), pal(7)])
plot.set_ylabel('#RML Executions')
buf = BytesIO()
plt.tight_layout()
plot.get_figure().savefig(buf, format="png")
st.image(buf)

# dataframe example
# modelId, score_name, score_value
# gpt4, f1, 0.9
# gpt4, f1, 0.8
# gpt4, f1, 0.7
# gpt4, f1, 0.9
# claude-1.3, f1, 0.9
# claude-1.3, f1, 0.8
# claude-1.3, f1, 0.7
# claude-1.3, f1, 0.6

# df = pd.DataFrame({
#     'modelId': ['gpt4', 'gpt4', 'gpt4', 'gpt4', 'claude-1.3', 'claude-1.3', 'claude-1.3', 'claude-1.3'],
#     'score_name': ['f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1'],
#     'score_value': [0.9, 0.8, 0.7, 0.6, 0.9, 0.8, 0.7, 0.6]
# })

# df = pd.DataFrame([
#     {'modelId': 'gpt4', 'score_name': 'f1', 'score_value': 0.9},
#     {'modelId': 'gpt4', 'score_name': 'f1', 'score_value': 0.8},
#     {'modelId': 'gpt4', 'score_name': 'f1', 'score_value': 0.7},
#     {'modelId': 'gpt4', 'score_name': 'f1', 'score_value': 0.6},
#     {'modelId': 'claude-1.3', 'score_name': 'f1', 'score_value': 0.9},
#     {'modelId': 'claude-1.3', 'score_name': 'f1', 'score_value': 0.8},
#     {'modelId': 'claude-1.3', 'score_name': 'f1', 'score_value': 0.7},
#     {'modelId': 'claude-1.3', 'score_name': 'f1', 'score_value': 0.6
# ])

# arr=[]
# for i in range(150):
#     arr.append({'modelId': random.choice(['gpt4', 'claude-1.3', 'claude-2.1']), 'score_name': 'f1', 'score_value': random.randint(1, 100)/100})


# meanprops = {"marker":"o",
#             "markerfacecolor":"white", 
#             "markeredgecolor":"black",
#             "markersize":"20"}
# def draw_plot(arr):
#     df = pd.DataFrame(arr)
#     plt.figure(figsize=(10, 5))
#     plt.ylim([-0.1, 1.1])
#     plt.ylabel('Score') 
#     sns.boxplot(data=df, x='modelId', y='score_value', hue='modelId',showmeans=True, boxprops=dict(alpha=.15), meanprops=meanprops,dodge=False, order=sorted(df['modelId'].unique()))
#     sns.stripplot(data=df, x='modelId', y='score_value', hue='modelId', jitter=True, dodge=False, marker='X',size=15,order=sorted(df['modelId'].unique()))

#     buf = BytesIO()
#     plt.savefig(buf, format="png")
#     st.image(buf,"some")


# draw_plot(arr)
# draw_plot(arr)


