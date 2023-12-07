import nipyapi as niapi

#----------------------------------------------------------------------------------------------------------
''' 1 '''
''' настройка соединения '''
def setConfigNifi(host, port):
    niapi.config.nifi_config.host = 'http://'+host+':'+str(port)+'/nifi-api'

#----------------------------------------------------------------------------------------------------------
''' 2 '''
''' root '''
def getRootProcessId():
    return niapi.canvas.get_root_pg_id()

def getRootProcessGroup(rootProcessId):
    return niapi.canvas.get_process_group(rootProcessId,'id')

#----------------------------------------------------------------------------------------------------------
def getAllProcessGroupList(RootPgId):    
    AllProcessGroup = niapi.canvas.list_all_process_groups(RootPgId)
    print('\nPROCESSOR GROUP [canvas.list_all_process_groups]:')
    AllProcessGroupList = []
    for group in AllProcessGroup:
        AllProcessGroupList.append([str(group.status.name),str(group.id)])
        print('%30s%3s%-40s' % (str(group.status.name),' : ',str(group.id)))
    return AllProcessGroupList

#----------------------------------------------------------------------------------------------------------
''' 3 '''
''' шаболоны на хосте '''
def getAllTemplateList():
    AllTemplate = niapi.templates.list_all_templates(native=True)    
    print('\nTEMPLATE LIST [templates.list_all_templates]:')
    for tmp in AllTemplate.templates:       
        print('%30s%3s%-40s' % (tmp.template.name,' : ',tmp.template.id))

#----------------------------------------------------------------------------------------------------------
''' 4 '''
''' создание группы, разворачивание шаблона '''
def createGrpoupDeployTemplate(rootProcessGroup, groupName,idTemplate, topX, leftY):       
    userProcessorGroup = niapi.canvas.create_process_group(rootProcessGroup, groupName,(topX,leftY))    
    niapi.templates.deploy_template(userProcessorGroup.id,idTemplate,100,100)
    return userProcessorGroup.id

#----------------------------------------------------------------------------------------------------------
''' 5 '''
''' список процессоров в группе '''
def getProcessorInGroup(idGroupName):
    listProcessors = niapi.canvas.list_all_processors(idGroupName)
    print('\nProcessor in Group:')
    processorsTmp = []
    processorsList = []
    for processor in listProcessors:
        print('%30s%3s%-40s' % (processor.status.name, " : ", processor.id))
        processorsTmp.append(processor.status.name)
        processorsTmp.append(processor.id)
        processorsTmp.append(processor)
        processorsList.append(processorsTmp)
        processorsTmp = []
    return processorsList

#----------------------------------------------------------------------------------------------------------
''' 6 '''
''' список парамтеров процессора '''
def getProcessorProperties(idGroupName, nameProcessor):
    listProcessors = niapi.canvas.list_all_processors(idGroupName)
    propertiesProcessor = []
    for processor in listProcessors:
        if processor.status.name == nameProcessor:
            print("\n" + processor.status.name + " :")
            propertiesProcessor = processor
    print(propertiesProcessor.component.config.properties)


#----------------------------------------------------------------------------------------------------------
''' 7 '''
''' настройка процессора '''
def setProperties(groupName, nameProcessor, propertiesKey, propertiesValue):
    processorsGroup = niapi.canvas.get_process_group(groupName)
    listProcessors = niapi.canvas.list_all_processors(processorsGroup.id)    
    for processor in listProcessors:
        if processor.status.name == nameProcessor:            
            propertiesProcessor = processor.component.config.properties
            configProperties = processor.component.config
            propertiesProcessor[propertiesKey] = propertiesValue    
            configProperties.properties = propertiesProcessor
            niapi.canvas.update_processor(processor ,configProperties)
            niapi.canvas.purge_process_group(processorsGroup, stop = True)
   
#----------------------------------------------------------------------------------------------------------
''' 8 '''
''' запуск группы '''
def startGroup(groupName):
    niapi.canvas.schedule_process_group(niapi.canvas.get_process_group(groupName,'id'), True)

#----------------------------------------------------------------------------------------------------------
''' 9 '''
''' удаление группы группы '''
def removeGroup(groupName):
    niapi.canvas.delete_process_group(niapi.canvas.get_process_group(groupName), force = True, refresh = True)

#----------------------------------------------------------------------------------------------------------



    
#----------------------------------------------------------------------------------------------------------
def step_01a_createGrp(rootProcessGroup, groupName, topX, leftY):    
    # Create user processor group    
    UserProcessorGroup = niapi.canvas.create_process_group(RootProcessGroup, groupName,(topX,leftY),groupName)
    return UserProcessorGroup

#----------------------------------------------------------------------------------------------------------
def step_01b_deployTmpl(idGroupName, idTemplate, leftX, topY):
    # Deploy templates
    DeployTemptate = niapi.templates.deploy_template(idGroupName, idTemplate, leftX, topY)

    deployDeviceId = str(DeployTemptate)
    deployDeviceId = deployDeviceId[deployDeviceId.index('source'):2470]
    deployDeviceId = deployDeviceId[deployDeviceId.index('group_id')+len('group_id')+4:]
    deployDeviceId = deployDeviceId[:36]
    #print('\nDevice group id: ',deployDeviceId)
    return DeployTemptate, deployDeviceId


















