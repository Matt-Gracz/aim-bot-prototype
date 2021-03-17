import commonObjsAndFuncs as common
import parsingFuncs as pfunc

#todo: design issues to address - not user friendly, global variables dangling everywhere, data format validation,
#                                 implement python package guidelines,
#                                 and there might be performance scalability issues for lots of data; it takes
#                                 ~10 minutes to enter in ~100 data points of inventory for example, oh and
#                                 since the codebase is growing, refactor into sub-libraries, such as common, logging, etc...

###MAIN USER FUNCS
###These are the main functions the user should be using, unless they need
###some sort of customization
def initComsDriverAndEng(fileName=fname, logFunc=common.logDebug):
	try:
		logFunc(message)("Parsing commands")
		commands = pfunc.parseCommandData(fileName)
		logFunc("Creating driver")
		driver = pfunc.createDriverInstance()
		logFunc("Creating Engine")
		engine = pfunc.createEngine()
		logFunc("Exiting initComsDriverAndEng")
	except:
		common.logError(message="Something went wrong in initComsDriverAndEng.", exception=e)

	#return a list instead of a tuple, as lists are iterable and mutable
	#Reason: while this is a helper function, we want to give some degree
	#of control over the returned data to promote customization where appropriate
	return [commands, driver, engine]

def execAllCommands(commands, driver, engine, logFunc=common.logDebug):
	try:
		for cmd in commands:
			logFunc("Parsing {}".format(str(cmd)))
			pfunc.execute(driver, engine, cmd)
	except Exception as e:
		common.logError(message="Something went wrong in execAllComs.", exception=e)

def executeBasicScript():
	execAllCommands(*initComsDriverAndEng())
	