import streamlit as st
import nipyapi


def deploy_template():
    template = nipyapi.templates.get_template(st.session_state.template_name)
    group = nipyapi.canvas.get_process_group(st.session_state.group_name)
    nipyapi.templates.deploy_template(template_id=template.id, pg_id=group.id)


nipyapi.config.nifi_config.host = 'http://127.0.0.1:8080/nifi-api'

templates_name = [
    template.template.name
    for template in nipyapi.templates.list_all_templates().templates
]

groups_names = [
    group.status.name
    for group in nipyapi.canvas.list_all_process_groups()
]

st.title('Play with apache-nifi')

with st.form('select nifi template'):
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
