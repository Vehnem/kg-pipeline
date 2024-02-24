import time
from os import listdir
from os.path import isfile, join
import streamlit as st
from llm4kg_core.llm.prompt import read_prompt_templates
from rdflib import Graph
import llm4kg_ui.util as util
import yaml
import traceback

st.set_page_config(layout="wide")

ONTOLOGY_FILENAME = '/workspace/papers/llm4rml/kg-pipeline/llm4kg_tests/resources/llm4rml/target_ontology.ttl'
PROMPTS_FILENAME = '/workspace/papers/llm4rml/kg-pipeline/llm4kg_tests/resources/llm4rml/prompts-rml.yaml'
SNIPPET_DIRECTORY = '/workspace/papers/llm4rml/kg-pipeline/target/data_snippets/'

def parse_query_parameter(key: str):
    # Retrieve the query parameter named 'id'
    id_value = st.query_params.get(key, None)
    return id_value


def generate_prompt_page():
    prompts = read_prompt_templates(PROMPTS_FILENAME)

    st.write('Edit Prompt Templates')
    st.markdown("---")

    prompt_list, prompt_display = st.columns([1, 3])

    prompt_id = parse_query_parameter('prompt')
    snippet_id = parse_query_parameter('snippet')

    with prompt_list:
        for p in prompts:
            hyperlink_url = f"?prompt={p}"
            if snippet_id:
                hyperlink_url = hyperlink_url + "&snippet=" + snippet_id
            st.markdown(f'<a target="_self" href="{hyperlink_url}">{p}: {prompts[p].description}</a>',unsafe_allow_html=True)

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

def generate_review_page():
    st.title('Instruction Review Page')

    text_area_content = st.text_area("Enter text here:")

    if st.button('Multiply by 2'):
        try:
            # Attempt to convert text area content to a number and multiply by 2
            multiplied_value = float(text_area_content) * 2
            st.write(f"The result is: {multiplied_value}")
        except ValueError:
            # Handle the case where the text is not a number
            st.error("Please enter a valid number.")

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

    if st.button('GENERATE'):
        try:
            with st.spinner('Generating...'):
                llm_output = util.execute_instruction(snippet_id, prompt_id)
            st.info("SUCCESS")
            st.write("Length: "+str(len(llm_output)))
            st.text_area("Completed",llm_output, disabled=True, height=1000)
        except:
            st.error("Something went wrong")
        

def generate_snippet_page():
    onlyfiles = [f for f in listdir(SNIPPET_DIRECTORY) if isfile(join(SNIPPET_DIRECTORY, f))]

    st.write('Edit Snippets')
    st.markdown("---")

    prompt_id = parse_query_parameter('prompt')
    snippet_id = parse_query_parameter('snippet')

    snippet_column, snippet_editor = st.columns([1, 3])

    with snippet_column:
        for f in onlyfiles:
            hyperlink_url = f"?snippet={f}"
            if prompt_id:
                hyperlink_url = hyperlink_url + "&prompt=" + prompt_id
            st.markdown(f'<a target="_self" href="{hyperlink_url}">{f}</a>',unsafe_allow_html=True)

    with snippet_editor:
        if snippet_id:
            with open(SNIPPET_DIRECTORY + snippet_id, 'r') as f:
                snippet_content = f.read()
            snippet_name = st.text_input("filename", snippet_id)
            snippet_content = st.text_area("Snippet", snippet_content, height=500)
            if st.button('SAVE SNIPPET'):
                try:
                    with open(SNIPPET_DIRECTORY + snippet_id, 'w') as f:
                        f.write(snippet_content)
                        with st.empty():
                            st.info("saved")
                            time.sleep(5)

                except ValueError:
                    # Handle the case where the text is not a number
                    st.error("Something went wrong")
        else:
            st.write("Please select a snippet from the list.")


if __name__ == '__main__':

    st.title("LLM4KG UI")

    # Define tabs for different pages
    tab_prompts, tab_review, tab_snippets, tab_ontology, tab_generate = "Prompt", "Review", "Snippets", "Ontology", "Generate"
    tab = st.tabs([tab_prompts, tab_snippets, tab_ontology, tab_generate, tab_review])

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
