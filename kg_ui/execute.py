import time
from os import listdir
from os.path import isfile, join
import streamlit as st
from kg_core.llm.prompt import read_prompt_templates
from kg_core.utils.mongodb import MongoConnection
from kg_core.config import Config
from kg_core.utils.output_parser import CodeBlockExtractor
from kg_tasks.map.rml_util import RML_Wrapper
from rdflib import Graph
import kg_ui.util as util
import yaml
import traceback
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from collections import defaultdict
import seaborn as sns
import pandas as pd
from kg_tasks.repair.rdfrepair import TurtleRepair


config = Config()

st.set_page_config(layout="wide")

ONTOLOGY_FILENAME = 'kg_tests/resources/llm4rml/target_ontology.ttl'
PROMPTS_FILENAME = 'kg_tests/resources/llm4rml/prompts-rml.yaml'
SNIPPET_DIRECTORY = 'target/data_snippets/'

def parse_query_parameter(key: str):
    # Retrieve the query parameter named 'id'
    id_value = st.query_params.get(key, None)
    return id_value

def on_change_prompt():
    st.query_params['prompt'] = st.session_state['prompt']

def generate_prompt_page():
    prompts = read_prompt_templates(PROMPTS_FILENAME)

    st.write('Edit Prompt Templates')
    st.markdown("---")

    prompt_list, prompt_display = st.columns([1, 3])

    prompt_id = parse_query_parameter('prompt')
    prompt_ids = sorted(list(prompts.keys()))
    prompt_idx = prompt_ids.index(prompt_id)
    # snippet_id = parse_query_parameter('snippet')

    with prompt_list:
        st.selectbox("Prompt", prompt_ids, key="prompt",index=prompt_idx, on_change=on_change_prompt)
            # hyperlink_url = f"?prompt={p}"
            # if snippet_id:
            #     hyperlink_url = hyperlink_url + "&snippet=" + snippet_id
            # st.markdown(f'<a target="_self" href="{hyperlink_url}">{p}: {prompts[p].description}</a>',unsafe_allow_html=True)

    with prompt_display:
        if prompt_id:
            a = st.radio("Show or Edit", ['Show', 'Edit'], 0)
            if a == 'Edit':
                id_value = st.text_input("ID", prompts[prompt_id].id)
                variables_value = st.text_input("Variables", ','.join(prompts[prompt_id].variables))
                description_value = st.text_input("Description", prompts[prompt_id].description)
                prompt_value = st.text_area("Prompt", prompts[prompt_id].prompt, height=500)
                if st.button('SAVE PROMPT'):
                    try:
                        # Attempt to convert text area content to a number and multiply by 2
                        # multiplied_value = float(text_area_content) * 2
                        # st.write(f"The result is: {multiplied_value}")
                        with open(PROMPTS_FILENAME, 'r') as yaml_file:
                            old_prompts =yaml.safe_load(yaml_file)
                        # with open(PROMPTS_FILENAME, 'w') as yaml_file:
                        new_prompt = {
                            'id': id_value,
                            'description': description_value,
                            'prompt': prompt_value,
                            'variables': variables_value.split(',')
                        }

                        existing = False
                        for idx, p in enumerate(old_prompts):
                            if p['id'] == id_value:
                                existing = True
                                old_prompts[idx] = new_prompt

                        if not existing:
                            old_prompts.append(new_prompt)

                        with open(PROMPTS_FILENAME, 'w') as yaml_file:
                            yaml.dump(old_prompts, yaml_file)
                        st.info("SUCCESS")
                        time.sleep(1)
                        # refresh page
                        st.experimental_rerun()
                    except ValueError:
                        # Handle the case where the text is not a number
                        st.error(traceback.format_exc())
                        st.error("Something went wrong")
                if st.button('DELETE PROMPT'):
                    try:
                        with open(PROMPTS_FILENAME, 'r') as yaml_file:
                            old_prompts =yaml.safe_load(yaml_file)
                        # with open(PROMPTS_FILENAME, 'w') as yaml_file:
                        new_prompts = [p for p in old_prompts if p['id'] != id_value]
                        with open(PROMPTS_FILENAME, 'w') as yaml_file:
                            yaml.dump(new_prompts, yaml_file)
                        st.info("SUCCESS")
                        time.sleep(1)
                        # refresh page
                        st.experimental_rerun()
                    except ValueError:
                        # Handle the case where the text is not a number
                        st.error("Something went wrong")

            else:
                st.markdown('- **Id:** '+prompts[prompt_id].id)
                st.markdown('- **Description:** '+prompts[prompt_id].description)
                st.markdown('- **Variables:** '+','.join(prompts[prompt_id].variables))
                st.markdown('---')
                st.write(len(prompts[prompt_id].prompt), ' characters')
                st.write(prompts[prompt_id].prompt)
            

        else:
            st.write("Please select a prompt from the list.")
    

def generate_ontology_page():
    st.write('TODO')
    with open(ONTOLOGY_FILENAME, 'r') as f:
        ontology_data_orig = f.read()
    ontology_data = st.text_area("Ontology", ontology_data_orig, height=500)

    if st.button('SAVE ONTOLOGY'):
        try:
            with open(ONTOLOGY_FILENAME, 'w') as f:
                f.write(ontology_data)
                graph = Graph()
                graph.parse(data=ontology_data, format="turtle")
                st.info("saved")
        except ValueError:
            # Handle the case where the text is not a number
            st.error("Something went wrong")


def on_change_snippet():
    st.query_params['snippet'] = st.session_state['snippet']

def generate_snippet_page():
    onlyfiles = sorted([f for f in listdir(SNIPPET_DIRECTORY) if isfile(join(SNIPPET_DIRECTORY, f))])

    st.write('Edit Snippets')
    st.markdown("---")

    # prompt_id = parse_query_parameter('prompt')
    snippet_id = parse_query_parameter('snippet')
    snippet_idx = onlyfiles.index(snippet_id)

    snippet_column, snippet_editor = st.columns([1, 3])

    # display_labels = []
    # for completion in completions:
    #     dl = f"[{str(completion['meta']['timestamp'])}] [{completion['meta'].get('prev_hash','')[0:5]}] [{completion['hash'][0:5]}] [{util.getModel(completion)}] {completion['meta']['prompt_id']} {completion['meta'].get('comment','')}"
    #     display_labels.append(dl)
    #     # display_labels.append(str(completion['meta']['timestamp'])) + ' ' + str(completion.get('id', ''))

    # def on_change_selecbox():
    #     res_box = st.session_state.get('result_box', None)
    #     if res_box:
    #         st.query_params['id'] = st.session_state.get('result_box', 0)

    # options = list(range(len(display_labels)))
    # value = st.selectbox("select result [timestamp] [prev_hash] [hash] [model] [prompt] \{metadata\}", options, format_func=lambda x: display_labels[x],index=tmp_id,key="result_box", on_change=on_change_selecbox())

    with snippet_column:
        st.selectbox("Snippet", onlyfiles, key="snippet", index=snippet_idx, on_change=on_change_snippet)
        # for f in onlyfiles:
        #     hyperlink_url = f"?snippet={f}"
        #     if prompt_id:
        #         hyperlink_url = hyperlink_url + "&prompt=" + prompt_id
        #     st.markdown(f'<a target="_self" href="{hyperlink_url}">{f}</a>',unsafe_allow_html=True)

    with snippet_editor:
        if snippet_id:
            with open(SNIPPET_DIRECTORY + snippet_id, 'r') as f:
                snippet_content = f.read()
            snippet_name = st.text_input("filename", snippet_id)
            snippet_content = st.text_area("Snippet", snippet_content, height=500)
            if st.button('SAVE SNIPPET'):
                try:
                    with open(SNIPPET_DIRECTORY + snippet_name, 'w') as f:
                        f.write(snippet_content)
                    with st.empty():
                        st.info("saved")
                        time.sleep(1)
                    st.rerun()
                except ValueError:
                    # Handle the case where the text is not a number
                    st.error("Something went wrong")
            if st.button('VALIDATE SNIPPET'):
                st.info('TODO')
        else:
            st.write("Please select a snippet from the list.")


def generate_generate_page():
    st.write('Generate LLM Output')
    st.markdown("---")

    # config_content, output_content = st.columns([1, 3])

    prompt_id = parse_query_parameter('prompt')
    snippet_id = parse_query_parameter('snippet')

    st.markdown(f"- **Prompt:** {prompt_id}")
    st.markdown(f"- **Snippet:** {snippet_id}")

    # with config_content:
    # prompts = read_prompt_templates(PROMPTS_FILENAME)
    # for p in prompts:
    #     hyperlink_url = f"?id={p}"
    #     st.markdown(f"[{p}: {prompts[p].description}]({hyperlink_url})")

    st.markdown("---")

    model_name = st.selectbox("Model", config.llm_models().keys())
    st.write(f'You selected {model_name}')

    model_parameter = st.text_area("TODO parameters", {})

    if st.button('GENERATE RML'):
        try:
            with st.spinner('Generating...'):
                llm_output = util.execute_instruction(model_name, snippet_id, prompt_id)
            st.info("SUCCESS")
            st.write("Length: "+str(len(llm_output)))
            st.text_area("Completed",llm_output, disabled=True, height=1000)
        except:
            # Handle the case where the text is not a number
            st.error("Something went wrong "+traceback.format_exc())

    if st.button('GENERATE REPAIR'):
        try:
            with st.spinner('Generating...'):
                llm_output = util.execute_repair_instruction(model_name, snippet_id, prompt_id)
            st.info("SUCCESS")
            st.write("Length: "+str(len(llm_output)))
            st.text_area("Completed",llm_output, disabled=True, height=1000)
        except:
            # Handle the case where the text is not a number
            st.error("Something went wrong "+traceback.format_exc())

    if st.button('COLD RUN'):
        st.write(len(util.build_prompt(snippet_id, prompt_id)), "prompt chracters")
        
def generate_review_page():
    st.write('Review Page')

    snippet_id = parse_query_parameter('snippet')
    # TODO
    result_id = parse_query_parameter("result")
    project_id = st.session_state.get('project', 'default')

    RESULT_IDX_KEY = 'result_idx'
    result_idx = int(st.query_params.get(RESULT_IDX_KEY, 0))
    # st.write("id: "+str(tmp_id))

    # print("journal_"+project_id)
    # print("journal_2024_03_01T15_55_49")
    completions = util.get_all_results("journal_"+project_id)

    # completion['meta']['prompt_vars']
    display_labels = []
    for completion in completions:
        dl = f"[{str(completion['meta']['timestamp'])}] [{completion['_id']}] [{completion['meta'].get('prev_hash','')[0:5]}] [{completion['hash'][0:5]}] [{util.getModel(completion)}] {completion['meta']['prompt_id']} {completion['meta'].get('comment','')}"
        display_labels.append(dl)
        # display_labels.append(str(completion['meta']['timestamp'])) + ' ' + str(completion.get('id', ''))

    def on_change_selecbox():
        res_box = st.session_state.get('result_box', None)
        if res_box:
            st.query_params[RESULT_IDX_KEY] = st.session_state.get('result_box', 0)

    options = list(range(len(display_labels)))
    value = st.selectbox("select result [timestamp] [prev_hash] [hash] [model] [prompt] \{metadata\}", options, format_func=lambda x: display_labels[x],index=result_idx,key="result_box", on_change=on_change_selecbox())
    # value = st.session_state.result_box

    # st.write(completions[value]['_id'])
    
    st.write(completions[value]['meta'])

    comment = st.text_input("comment", completions[value]['meta'].get('comment', ''))
    if st.button('SAVE COMMENT'):
        completions[value]['meta']['comment'] = comment
        util.update_doc(completions[value])
        # TODO without rerun
        st.rerun()
        # st.success("comment saved")
        # time.sleep(1)
        # st.rerun()


    with st.expander("see full prompt"): 
        st.text_area('prompt', completions[value]['prompt']['message'], disabled=True, height=500)

    with st.expander("see full completion"): 
        st.text_area('completion', completions[value]['completion']['message'], disabled=True, height=500)

    raw_completion = completions[value]['completion']['message']
    code = CodeBlockExtractor().extract_codeblocks_from_markdown(raw_completion)

    tr = TurtleRepair(code)
    tr.repair_prefixes()
    code = tr.data

    with st.expander("see extracted code block"): 
        st.code(code, language="turtle", line_numbers=True)

    st.markdown("---")

    if st.button('Parse and Eval RML'):
        try :
            rml_data: Graph = RML_Wrapper(Graph().parse(data=code, format="turtle"))
            st.success("VALID RDF")

            parsed_turtle = rml_data.getGraph().serialize(format="turtle")
            with st.expander("Parsed RDF Output"): 
                st.code(parsed_turtle, language="turtle", line_numbers=True)


            mapped = util.execute_mapping(rml_data.__str__(),snippet_id)
            st.success("MAPPING SUCCESS")

            with st.expander("Mapped RDF Output"): 
                st.code(mapped['output'], language="turtle", line_numbers=True)

            stats = util.createStatistics(mapped['output'])
            st.write(stats)
            # stats.update({'_id': completions[value]['_id']})
            # util.insert_eval(stats)
            # st.success('Saved to Evaluation Page')

        except Exception as e:
            st.error(e)

    if st.button('Repair'):
        model_name = util.getModel(completions[value])
        prev_hash = completions[value]['hash']

        with st.spinner('Repairing...'):
            result_entry = util.execute_repair_instruction(model_name, 'final-repair', code, prev_hash)

        st.success("Repair Finished")
        time.sleep(1)
        # st.query_params["result"] = result_entry['meta']
        st.rerun()


def plot_counts():

    df = pd.DataFrame({
        'no_repair': [2, 1],
        'one_reapir': [2, 3],
        'two_repair': [4, 2],
        'more_than_two_repair': [2, 4],
    }, index=['gpt4', 'gpt3'], columns=['no_repair', 'one_reapir', 'two_repair', 'more_than_two_repair'])
    st.write(df)

    # plot dataframe
    plot = df.plot(kind='bar', stacked=True, color=["lightgreen","lightblue","lightyellow","red"])
    plot.set_ylabel('Count')
    buf = BytesIO()
    plot.get_figure().savefig(buf, format="png")
    st.image(buf)

    df = pd.DataFrame({
        'crash': [2, 1],
        'no_triples': [2, 3],
        'triples': [4, 2],
    }, index=['gpt4', 'gpt3'], columns=['crash', 'no_triples', 'triples'])
    st.write(df)

    # plot dataframe
    plot = df.plot(kind='bar', stacked=True, color=["lightgreen","lightblue","lightyellow","red"])
    plot.set_ylabel('Count')
    buf = BytesIO()
    plot.get_figure().savefig(buf, format="png")
    st.image(buf)



meanprops = {"marker":"o",
            "markerfacecolor":"white", 
            "markeredgecolor":"black",
            "markersize":"10"}

medianprops = dict(linewidth=2.5) #{ 'alpha':1, 'marker': '-', 'markersize': 12}

finalModelNameByModelName = {
    'claude-3-opus-20240229' :'claude3',
    'gpt-4-0125-preview': 'gpt4'
}

def draw_plot(arr, caption,x=None, y=None):

    df = pd.DataFrame(arr)
    df = df.replace({'modelId':finalModelNameByModelName})
    df['score_value'] = df['score_value'].apply(lambda x: 1 if x > 1 else x)
    st.write(df)
    plt.figure(figsize=(df['modelId'].unique().__len__() , 4))

    sns.boxplot(data=df, x='modelId', y='score_value', hue='modelId',showmeans=True, boxprops=dict(alpha=.15), medianprops=medianprops,meanprops=meanprops,dodge=False, order=sorted(df['modelId'].unique()))
    sns.stripplot(data=df, x='modelId', y='score_value', hue='modelId', jitter=0.25, dodge=False, marker='x', alpha=0.7, s=5, linewidth=1, order=sorted(df['modelId'].unique()))

    plt.ylim([-0.1, 1.1])
    plt.ylabel('F1 Score') 
    plt.xlabel('')
    plt.title('')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    st.image(buf,caption=caption)



def plot_precision_recall_f1(score_name, scores):
    # TODO https://seaborn.pydata.org/tutorial/axis_grids.html

    if not score_name == "single_property_scores" and not score_name == "predicates_direct" and not score_name == "predicates_inverse":

        scores_by_model = defaultdict(list)
        for score in scores:
            scores_by_model[score['model']].append(score['f1'])

        # st.write(scores_by_model)

        arr = []
        for model in scores_by_model.keys():
            for score in scores_by_model[model]:
                arr.append({'modelId': str(model), 'score_name': 'f1', 'score_value': score})

        draw_plot(arr, score_name)

    else:
        scores_by_model = defaultdict(lambda: defaultdict(list))
        for score in scores:
            for k in score.keys():
                if str(k).startswith('http://'):
                    scores_by_model[score['model']][k].append(score[k]['f1'])
        

        for model in scores_by_model.keys():
            arr = []
            for property_name in scores_by_model[model]:
                p_name_short = property_name.split('/')[-1]
                x_scores = scores_by_model[model][property_name]
                for score in x_scores:
                    arr.append({'modelId': p_name_short, 'score_name': 'f1', 'score_value': score})

            draw_plot(arr, model+'_'+p_name_short)
        
            # scores_by_model[score['model']][score['property']].append(score['f1'])
        # draw_plot(arr, score_name)

    # df = pd.DataFrame.from_dict(scores_by_model, orient='index')
    # df = df.transpose()
                
    # # st.write(len(scores_by_model.keys()))

    # color_pallet = sns.color_palette("muted", 6)
    # fig, axes = plt.subplots(1, len(scores_by_model.keys()), figsize=(len(scores_by_model.keys())*2, 4), sharey=True)

    # # print(scores_by_model.keys())

    # if len(scores_by_model.keys()) == 1:
    #     # y=str(list(scores_by_model.keys())[0])
    #     sns.boxplot(data=df, ax=axes, y=list(scores_by_model.keys())[0], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black", "markersize":"12"})
    #     axes.set_title(list(scores_by_model.keys())[0])
    #     axes.set_ylabel('F1 Score')
    #     axes.set(ylim=(-0.1, 1.1))

    # else:
    #     for idx, key in enumerate(scores_by_model.keys()):
    #         sns.boxplot(data=df, ax=axes[idx], y=str(key), showmeans=True, boxprops=dict(alpha=.15), meanprops={"marker":"o","markerfacecolor":"white", "markeredgecolor":"black", "markersize":"12"}, color=color_pallet[idx], dodge=True)
    #         # sns.stripplot(data=df, x=axes[idx], y=str(key), jitter=True, dodge=True, marker='X') 
    #         axes[idx].set_title(label=str(key),)
    #         axes[idx].set_ylabel('F1 Score')
    #         axes[idx].set(ylim=(-0.1, 1.1))

    # # save the plot
    # buf = BytesIO()
    # fig.savefig(buf, format="png")
    # st.image(buf,score_name)

    with st.expander("Evaluation Scores by Model "+score_name):
        st.write(scores)


def generate_evaluation_page():

    project_id = st.session_state['project']
    stats = list(util.getEvaluationStats("evaluation_"+project_id))
    
    # plot_counts()

    models = set()
    score_map = defaultdict(list)
    for stat in stats:
        for k in stat.keys()-{'_id','model'}:
                models.add(stat['model'])
                # st.write(k)
                stc = stat[k]
                stc.update({'model': stat['model']})
                score_map[k].append(stc)        

    options = st.multiselect("Select Scores", sorted(list(score_map.keys()-{'_id','model'})))

    st.write('models', models)
    for score_name in sorted(score_map.keys()):
        if score_name == '_id':
            continue
        if score_name not in options:
            continue
        plot_precision_recall_f1(score_name, score_map[score_name])

    st.caption('All Scores')

    for stat in stats:
        stat.update({'select': False}) 

    df = st.data_editor(stats)

    # st.markdown("""
    #             <style>
    #                 div[data-testid="column"] {
    #                     width: fit-content !important;
    #                     flex: unset;
    #                 }
    #                 div[data-testid="column"] * {
    #                     width: fit-content !important;
    #                 }
    #             </style>
    #             """, unsafe_allow_html=True)
    
    colx1, colx2, colx3 = st.columns([1,1,1])

    with colx1:
        if st.button('Delete Selected'):
            for stat in df:
                if stat['select']:
                    util.remove_eval(stat['_id'])
            st.success('Removed (reload in a few seconds)')
            time.sleep(1)
            st.rerun()

    with colx2:
        if st.button('Recalculate All'):
            st.info('TODO')

    # width = st.sidebar.slider("plot width", 1, 25, 3)
    # height = st.sidebar.slider("plot height", 1, 25, 1)

    # arr = np.random.normal(1, 1, size=100)
    # fig, ax = plt.subplots(figsize=(width, height),)
    # ax.hist(arr, bins=20)

    # buf = BytesIO()
    # fig.savefig(buf, format="png")
    # st.image(buf,"test")

def on_change_project():
    st.query_params['id'] = 0
    st.query_params['project'] = st.session_state['project']

if __name__ == '__main__':

    st.title("LLM4KG Web UI")

    st.selectbox("Select Project", util.projects(), key="project", on_change=on_change_project)

    # Define tabs for different pages
    tab_prompts, tab_review, tab_snippets, tab_ontology, tab_generate, tab_evaluation = "Prompt", "Review", "Snippets", "Ontology", "Generate", "Evaluation"
    tab = st.tabs([tab_prompts, tab_snippets, tab_ontology, tab_generate, tab_review, tab_evaluation])

    with tab[0]:  # Prompt tab content
        generate_prompt_page()

    with tab[1]:  # Snippets tab content
        generate_snippet_page()

    with tab[2]:  # Ontology tab content
        generate_ontology_page()

    with tab[3]:  # Generate tab content
        generate_generate_page()

    with tab[4]:  # Review tab content
        generate_review_page()

    with tab[5]: # Evaluation tab content
        generate_evaluation_page()

