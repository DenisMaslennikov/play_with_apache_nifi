import nipyapi as niapi

HOST = '10.72.102.96'
PORT = 8080

niapi.config.nifi_config.host = 'http://'+HOST+':'+str(PORT)+'/nifi-api'

RootPgId = niapi.canvas.get_root_pg_id()
print('RootPgId: ',RootPgId)
RootProcessGroup = niapi.canvas.get_process_group(RootPgId,'id')
print(RootProcessGroup)


# ok
# ProcessorGroup List
AllProcessGroup = niapi.canvas.list_all_process_groups(RootPgId)
print('\nPROCESSOR GROUP [canvas.list_all_process_groups]:')
AllProcessGroupList = []
for group in AllProcessGroup:
    AllProcessGroupList.append([str(group.status.name),str(group.id)])
    print('%30s%3s%-40s' % (str(group.status.name),' : ',str(group.id)))


# ok
# Template List
AllTemplate = niapi.templates.list_all_templates(native = True)
TemplateList = AllTemplate.templates
print('\nTEMPLATE LIST [templates.list_all_templates]:')
for item in TemplateList:
    template = item.template
    print('%30s%3s%-40s' % (template.name,' : ',template.id))



#tmpModbusTCP = niapi.templates.get_template_by_name('ModbusTCP_ExecuteScript_v01')
#tmpIdModbusTCP = tmpModbusTCP.id

#tmpModbusTCP_JSON = niapi.templates.get_template_by_name('ModbusTCP_JSON_ExScr_v01')
#tmpIdModbusTCP_JSON = tmpModbusTCP_JSON.id


#----------------------------------------------------------------------------------------------------------
def step_01_createGrp_deployTmpl(groupName,idTemplate):
    #'''   
    # Create user processor group    
    UserProcessorGroup = niapi.canvas.create_process_group(RootProcessGroup, groupName,(400,100),'create from python')
    # Deploy templates
    niapi.templates.deploy_template(UserProcessorGroup.id, idTemplate, 100,100)
    # Check
    IdUserProcessorGroup = AllProcessGroup[5].id #id UserProcessorGroup
    prc_UserProcessorGroup = niapi.canvas.list_all_processors(IdUserProcessorGroup)
    print("\nPROCESSOR in UserProcessorGroup:")
    for processor in prc_UserProcessorGroup:
        print('%30s%3s%-40s' % (str(processor.status.name),' : ',str(processor.id)))
    #'''

#----------------------------------------------------------------------------------------------------------
def step_02_processor_config(groupName,properties):
    #'''    
    ProcessorUserGroup = niapi.canvas.get_process_group(groupName)
    list_ProcessorUserGroup = niapi.canvas.list_all_processors(ProcessorUserGroup.id)
    print('\nProcessor in UserGroup:')
    ProcessorGenFile = []
    for i in list_ProcessorUserGroup:
        if i.status.name == 'GenerateFlowFile':
            ProcessorGenFile = i            
        print(i.status.name)
    propGenerateFlowFile = ProcessorGenFile    
    props = propGenerateFlowFile.component.config.properties
    props['generate-ff-custom-text'] = properties
    config = propGenerateFlowFile.component.config
    config.properties = props
    niapi.canvas.update_processor(propGenerateFlowFile,config)
    niapi.canvas.purge_process_group(ProcessorUserGroup, stop=True) # empty queue
    #'''
 

GroupName = 'New-User'
#step_01_createGrp_deployTmpl(GroupName, tmpModbusTCP.id)
#step_02_processor_config(GroupName, '10.1.216.67:502:25:5')  #old: 10.1.216.103:502:25:15
#niapi.canvas.schedule_process_group(niapi.canvas.get_process_group(GroupName).id, True)                    # ok - ШАГ 3: запуск группы
#niapi.canvas.delete_process_group(niapi.canvas.get_process_group(GroupName), force = True, refresh = True) # ok - ШАГ 4: удаление группы



