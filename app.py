import streamlit as st
import nipyapi


def deploy_template():
    template = nipyapi.templates.get_template(st.session_state.template_name)
    group = nipyapi.canvas.get_process_group(st.session_state.group_name)
    nipyapi.templates.deploy_template(template_id=template.id, pg_id=group.id)

def setup_nifi_parameters():
    parameters_group = nipyapi.parameters.get_parameter_context(
        st.session_state.parameters_group_name
    )
    for parameter in parameters_group.component.parameters:
        parameter.parameter.value = st.session_state[parameter.parameter.name]
    nipyapi.parameters.update_parameter_context(parameters_group)


nipyapi.config.nifi_config.host = 'http://127.0.0.1:8080/nifi-api'

templates_name = [
    template.template.name
    for template in nipyapi.templates.list_all_templates().templates
]

groups_names = [
    group.status.name
    for group in nipyapi.canvas.list_all_process_groups()
]

parameters_group_name = [
    param_group.component.name
    for param_group in nipyapi.parameters.list_all_parameter_contexts()
]

st.title('Play with apache-nifi')

with st.form('select NIFI template'):
    st.selectbox(
        'Выбор шаблона',
        options=templates_name,
        key='template_name',
    )
    st.selectbox(
        'Выбор группы',
        options=groups_names,
        key='group_name',
    )
    st.form_submit_button(
        label='OK',
        on_click=deploy_template,
    )

with st.form('Select NIFI parameters'):

    st.selectbox(
        'Выбор группы параметров',
        options=parameters_group_name,
        key='parameters_group_name'
    )
    parameters_group = nipyapi.parameters.get_parameter_context(
        st.session_state.parameters_group_name
    )
    st.write(
        parameters_group.component.description
        if parameters_group.component.description else ''
    )
    for parameter in parameters_group.component.parameters:
        st.text_input(
            parameter.parameter.name,
            parameter.parameter.value,
            key=parameter.parameter.name,
        )
    st.form_submit_button(label='OK', on_click=setup_nifi_parameters)

