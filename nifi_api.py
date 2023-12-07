import nipyapi as niapi
import nifi_api_fun as fn


HOST = '10.72.102.96'
PORT = 8080

''' 1 '''
''' настройка соединения '''
fn.setConfigNifi(HOST, PORT)

''' 2 '''
''' root '''
rootProcessId = fn.getRootProcessId()
rootProcessGroup = fn.getRootProcessGroup(rootProcessId)
print(rootProcessGroup)

fn.getAllProcessGroupList(rootProcessId) # необязательно


''' 3 '''
''' шаболоны на хосте '''
fn.getAllTemplateList()
idTemplate = 'b677ebd0-d93a-4582-935c-7503b280ce94' 


''' 4 '''
''' создание группы, разворачивание шаблона '''
groupName = 'MTS-NewUserGropup'
idGroupName = fn.createGrpoupDeployTemplate(rootProcessGroup, groupName, idTemplate, 800, 100)
print("Id " + groupName + " : " + idGroupName)


''' 5 '''
''' список процессоров в группе '''
processorsList = fn.getProcessorInGroup(idGroupName)
print()
for processor in processorsList:
    print('%30s%3s%-40s' % (processor[2].status.name, " : ", processor[2].id))
    print(processor[2])


''' 6 '''
''' список парамтеров процессора '''
fn.getProcessorProperties(idGroupName, 'IoTNettyProcessor')


''' 7 '''
''' настройка процессора '''
fn.setProperties(groupName, 'IoTNettyProcessor', 'SERVER_ADDRESS', '0.0.0.0')
fn.setProperties(groupName, 'IoTNettyProcessor', 'SERVER_PORT', '9000')
fn.setProperties(groupName, 'IoTNettyProcessor', 'CYCLE_TIME', '60')


''' 8 '''
''' запуск группы '''
#fn.startGroup(groupName)


''' 9 '''
''' удаление группы '''
#fn.removeGroup(groupName)


