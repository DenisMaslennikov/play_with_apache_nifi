import re

import streamlit as st
import nipyapi


MIN_PARAMETERS_AMOUNT = 0
MAX_PARAMETERS_AMOUNT = 100
DEFAULT_PARAMETERS_AMOUNT = 1

PARAMETER_NAME_STRING = lambda  index: f'parameter_name_{index}'
PARAMETER_VALUE_STRING = lambda  index: f'parameter_value_{index}'
PARAMETER_DESCRIPTION_STRING = lambda  index: f'parameter_description_{index}'

nipyapi.config.nifi_config.host = 'http://127.0.0.1:8080/nifi-api'

templates_names = [
    template.template.name
    for template in nipyapi.templates.list_all_templates().templates
]

groups_names = [
    group.status.name
    for group in nipyapi.canvas.list_all_process_groups()
]

parameters_context_names = [
    param_group.component.name
    for param_group in nipyapi.parameters.list_all_parameter_contexts()
]


def deploy_template():
    template = nipyapi.templates.get_template(st.session_state.template_name)
    group = nipyapi.canvas.get_process_group(
        st.session_state.group_name_for_template, greedy=False
    )
    nipyapi.templates.deploy_template(template_id=template.id, pg_id=group.id)


def setup_nifi_parameters_for_select_context():
    parameters_context = nipyapi.parameters.get_parameter_context(
        st.session_state.parameters_context_name, greedy=False
    )
    for parameter in parameters_context.component.parameters:
        parameter.parameter.value = st.session_state[parameter.parameter.name]
    nipyapi.parameters.update_parameter_context(parameters_context)


def create_parameters_context(form):
    parameters = []
    for index in range(st.session_state.parameters_count):
        name = st.session_state[PARAMETER_NAME_STRING(index)]
        if not(re.fullmatch('[a-zA-Z0-9 _-]+', name)):
            form.error(
                'Название параметра может содержать буквы a-Z, цифры и '
                'символы -_'
            )
            return None
        parameters.append(nipyapi.parameters.prepare_parameter(
            name=name,
            value=st.session_state[PARAMETER_VALUE_STRING(index)],
            description=st.session_state[PARAMETER_DESCRIPTION_STRING(index)]
        ))
    nipyapi.parameters.create_parameter_context(
        name=st.session_state.context_name,
        description=st.session_state.context_description,
        parameters=parameters,
    )


def assign_parameter_context_to_processor_group():
    group = nipyapi.canvas.get_process_group(
        st.session_state.group_name_for_parameter_context, greedy=False
    )
    parameter_context = nipyapi.parameters.get_parameter_context(
        st.session_state.parameter_context_name_for_group, greedy=False
    )
    nipyapi.parameters.assign_context_to_process_group(
        group, parameter_context.id
    )


def remove_context_from_process_group():
    group = nipyapi.canvas.get_process_group(
        st.session_state.group_name_for_context_remove, greedy=False
    )
    nipyapi.parameters.remove_context_from_process_group(group)


def delete_parameter_context():
    parameter_context = nipyapi.parameters.get_parameter_context(
        st.session_state.parameter_context_name_for_delete, greedy=True
    )
    nipyapi.parameters.delete_parameter_context(parameter_context)


st.title('Play with apache-nifi')

with st.form('select NIFI template'):
    st.selectbox(
        'Выбор шаблона',
        options=templates_names,
        key='template_name',
    )
    st.selectbox(
        'Выбор группы',
        options=groups_names,
        key='group_name_for_template',
    )
    st.form_submit_button(
        label='OK',
        on_click=deploy_template,
    )

left, right = st.columns(2)

with left:
    parameters_count = st.number_input(
        label='Количество параметров:',
        min_value=MIN_PARAMETERS_AMOUNT,
        max_value=MAX_PARAMETERS_AMOUNT,
        value=DEFAULT_PARAMETERS_AMOUNT,
        key='parameters_count',
    )
    create_context_form =st.form('Create NIFI parameters context')
    with create_context_form:
        st.text_input(
            label='Название контекста',
            key='context_name',
        )
        st.text_area(
            label='Описание контекста',
            key='context_description',
        )
        for index in range(parameters_count):
            sub_left, sub_right = st.columns(2)
            with sub_left:
                st.text_input(
                    label=f'Имя параметра #{index + 1}',
                    key=PARAMETER_NAME_STRING(index),
                )
            with sub_right:
                st.text_input(
                    label=f'Значение параметра #{index + 1}',
                    key=PARAMETER_VALUE_STRING(index),
                )
            st.text_area(
                label='Описание параметра',
                key=PARAMETER_DESCRIPTION_STRING(index),

            )

        st.form_submit_button(
            'OK',
            on_click=create_parameters_context,
            args=(create_context_form,),
        )

with right:
    parameters_context_name = st.selectbox(
        'Выбор контекста параметров',
        options=parameters_context_names,
        key='parameters_context_name',

    )
    with st.form('Change NIFI parameters'):
        parameters_context = nipyapi.parameters.get_parameter_context(
            parameters_context_name, greedy=False
        )
        st.write(
            parameters_context.component.description
            if parameters_context.component.description else ''
        )
        for parameter in parameters_context.component.parameters:
            st.text_input(
                parameter.parameter.name,
                parameter.parameter.value,
                help=parameter.parameter.description,
                key=parameter.parameter.name,
            )
        st.form_submit_button(
            label='OK',
            on_click=setup_nifi_parameters_for_select_context
        )

with left:
    with st.form('Assign parameter context to processor group'):
        st.selectbox(
            label='Выбор группы',
            options=groups_names,
            key='group_name_for_parameter_context',
        )
        st.selectbox(
            'Выбор контекста параметров',
            parameters_context_names,
            key='parameter_context_name_for_group',
        )
        st.form_submit_button(
            label='OK',
            on_click=assign_parameter_context_to_processor_group,
        )
with right:
    with st.form('Remove context from processor group'):
        st.selectbox(
            label='Выбор группы для удаления контекста',
            options=groups_names,
            key='group_name_for_context_remove',
        )
        st.form_submit_button(
            label='Удалить',
            on_click=remove_context_from_process_group,
        )
    with st.form('Delete context group'):
        st.selectbox(
            label='Выбор контекста для удаления',
            options=parameters_context_names,
            key='parameter_context_name_for_delete',
        )
        st.form_submit_button(
            label='Удалить',
            on_click=delete_parameter_context,
        )
