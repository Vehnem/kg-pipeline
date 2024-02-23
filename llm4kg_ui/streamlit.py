import streamlit as st
from llm4kg_core.llm.prompt import read_prompt_templates

st.set_page_config(layout="wide")

def parse_query_parameter_id():
    # Retrieve the query parameter named 'id'
    id_value = st.query_params.get('id', None)
    return id_value


def generate_prompt_page():
    prompts = read_prompt_templates('llm4kg_tests/prompts/prompts-rml.yaml')

    st.write('Edit Prompt Templates')
    st.markdown("---")

    prompt_list, prompt_display = st.columns([1, 3])

    with prompt_list:
        for p in prompts:
            hyperlink_url = f"?id={p}"
            st.markdown(f"[{p}: {prompts[p].description}]({hyperlink_url})")
            # s, unsafe_allow_html=True)

    with prompt_display:
        prompt_id = parse_query_parameter_id()
        if prompt_id:
            a = st.radio("Show or Edit", ['Show', 'Edit'], 0)
            if a == 'Edit':
                st.text_input("ID", prompts[prompt_id].id)
                st.text_input("Variables", ','.join(prompts[prompt_id].variables))
                st.text_input("Description", prompts[prompt_id].description)
                st.text_area("Prompt", prompts[prompt_id].prompt)
                if st.button('SAVE'):
                    try:
                        # Attempt to convert text area content to a number and multiply by 2
                        # multiplied_value = float(text_area_content) * 2
                        # st.write(f"The result is: {multiplied_value}")
                        st.info("TODO")
                    except ValueError:
                        # Handle the case where the text is not a number
                        st.error("Something went wrong")
            else:
                st.title('ID: '+prompts[prompt_id].id)
                st.write('Description: '+prompts[prompt_id].description)
                st.write('Variables:'+','.join(prompts[prompt_id].variables))
                st.write(prompts[prompt_id].prompt)

        else:
            st.write("Please select a prompt from the list.")
    

    

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


if __name__ == '__main__':

    st.title("LLM4KG UI")

    # Define tabs for different pages
    tab_prompts, tab_review, tab_snippets, tab_ontology, tab_generate = "Prompt", "Review", "Snippets", "Ontology", "Generate"
    tab = st.tabs([tab_prompts, tab_snippets, tab_ontology, tab_generate, tab_review])

    with tab[0]:  # Home tab content
        generate_prompt_page()

    with tab[1]:  # About tab content
        st.write("TODO")

    with tab[2]:  # Home tab content
        st.write("TODO")

    with tab[3]:  # About tab content
        st.write("TODO")

    with tab[4]:  # Home tab content
        generate_review_page()
