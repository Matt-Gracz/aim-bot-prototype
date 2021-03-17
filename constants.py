#All constants the codebase needs should live here.  Big TODO is to refactor embedded constants into
#this file.  But low priority for now.
waitIntervalInSecs = .75
explicitWaitInSecs = 5
url = "http://127.0.0.1:8080/fmax/screen/WORKDESK"
fname = 'test-excel-file.xlsx'
defaultOutputfileName = "parsed-preflattened-commands.xlsx"
DEBUG = False

### todo: meta-program this junk away in a dedicated class
### we want to encourage getter/setter invocations rather than direct variable
### references, but I don't want to write a getter/setter everytime I add a new
### variable, so I want to meta-program the problem away by coding in the ability
### to call constants.getSet<variableName>(), for any variable available in the lib
### at runtime but it's super low priority.  It'll require digging into the properties
### of the Class "Class"
### --mgracz
# def getSetWaitInterval(newWI = None):
#   waitIntervalInSecs = newWI if newWI is not None else waitIntervalInSecs
#   return waitIntervalInSecs
# def getSetExplicitWait(newEW = None):
#   explicitWaitInSecs = newEW if newEW is not None else explicitWaitInSecs
#   return waitIntervalInSecs
# def getSetUrl(newURL = None):
#   url = newURL if newURL is not None else url
#   return url
# def getSetFileName(newFN = None):
#   fname = newFN if newFN is not None else fname
#   return fname
# def getSetDebugLevel(newDL = None):
#   DEBUG = newDL if not newDL is not None else DEBUG
#   return DEBUG