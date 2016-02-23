import os, json
from com.xebialabs.deployit.plugin.api.reflect import Type

dir = xlPlugins  #from task in XLR
oldFiles = os.listdir(dir)

jsonDir= '/pluginlog/'

fullPath = dir+jsonDir

if not os.path.exists(fullPath):
    os.makedirs(fullPath)

jsonFile = dir+jsonDir+"plugins.json"
inputJson = jsonFile
phaseName = 'Input Plugin Information'
phase = getCurrentPhase()
nextPhase = "Update Plugins"

release = getCurrentRelease()
releaseId = release.id
#print "Current Release: ", releaseId
#print "Phase ID: ", phase.id

newPhase = phaseApi.searchPhasesByTitle(nextPhase, str(release.id))
targetPhase = str(newPhase[0])

#print "New Phase: ", targetPhase

#print jsonFile

print "\nCurrent Phase: ", getCurrentPhase()
print "\n"

response = []

'''
#if plugins.json already exists but is empty remove it
if os.path.isfile(jsonFile) is True and os.stat(jsonFile).st_size == 0: #if plugins.json exists and is empty, remove it
    print "File exists but is empty ... Removing " + jsonFile + "!"
    os.remove(jsonFile)
    # NOT FINISHED: Add some logic to produce the new json file
'''

if os.path.isfile(jsonFile) is True and os.stat(jsonFile).st_size != 0: # if plugins.json exists and is not empty read the file
    print "File exists ... reading plugin data and creating update tasks!\n"

    task = taskApi.newTask("mgmt.JsonCleanup")
    task.title = "Backup Previous Plugin Data"
    taskApi.addTask(targetPhase, task)

    task = taskApi.newTask("xlrelease.Task")
    task.title = "Enter new plugin versions in tasks below"
    taskApi.addTask(targetPhase, task)

    with open(jsonFile) as json_data:
        d = json.load(json_data)
        json_data.close()
        #pprint(d)

        for key in d:
            #print key['fileName']
            plugin = key['plugin']
            curVers = key['currentVersion']
            fName = key['fileName']
            updateType = key['updateType']
            gitRepo = key['gitRepo']
            pluginLocation = key['pluginLocation']

            print "FILE: ", fName
            print "\n"

            task = taskApi.newTask("mgmt.UpdatePlugins")
            task.title = "Update "+plugin
            task.pythonScript.pluginName = plugin #Plugin name variable
            task.pythonScript.pluginFile = fName #Plugin full file name variable
            task.pythonScript.currentVersion = curVers #currently installed version variable
            task.pythonScript.updateType = updateType #type of update for plugin (local, git, etc.)
            task.pythonScript.gitRepo = gitRepo #the name of the git repo if the plugin release is stored in Git
            task.pythonScript.pluginLocation = pluginLocation #location of the new plugin file either a URL or local or shared path
            taskApi.addTask(targetPhase, task)

else: #scan the specified plugins folder for all existing plugins and create new tasks to update

    for oldInstalledPlugins in oldFiles:
        #print oldInstalledPlugins
        oldPlugin = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 5)[0].rsplit('-', 1)[0]
        oldFtype = oldInstalledPlugins.replace(dir, ' ').rsplit('.', 1)[-1]
        oldVersion = oldInstalledPlugins.replace(dir, ' ').rsplit('-', 1)[-1].replace('.' + oldFtype, "")

        if (oldPlugin != '') and (oldPlugin != 'readme') and (oldPlugin != 'lm'): # ignore any files that are not actually plugins
            response.append({'plugin': oldPlugin, 'currentVersion' : oldVersion, 'newVersion': 'null','lastVersion': 'NA', 'updateType': 'Enter Manually', 'fileName': oldInstalledPlugins, 'gitRepo': 'Enter Manually', 'pluginLocation': 'Enter Manually'})
            #print "Old: ", oldPlugin
            print "Old " + oldPlugin + " version is "+ oldVersion + " is currently installed!\n"
            #create the task
            task = taskApi.newTask("mgmt.UpdatePlugins")
            task.title = "Update "+oldPlugin
            task.pythonScript.pluginName = oldPlugin #Plugin name variable
            task.pythonScript.pluginFile = oldInstalledPlugins #Plugin full file name variable
            task.pythonScript.currentVersion = oldVersion #currently installed version variable
            taskApi.addTask(targetPhase, task)

    #create json file
    outputFile = open(jsonFile, "w+")
    json_data = json.dumps(response, outputFile, indent=4)
    outputFile.write(json_data)
    outputFile.close()

task = taskApi.newTask("mgmt.RelinkPlugins")
task.title = "Relink Plugins Folder"
taskApi.addTask(targetPhase, task)

