import commonObjsAndFuncs as common
import parsingFuncs as pfunc

#todo: design issues to address - not user friendly, global variables dangling everywhere, messy command init structure,
#                                 debugging is weird, data format validation, implement python package guidelines,
#                                 and there might be performance scalability issues for lots of data; it takes
#                                 ~10 minutes to enter in ~100 data points of inventory for example, oh and
#                                 since the codebase is growing, refactor into sub-libraries, such as common, logging, etc...

###MAIN USER FUNCS
###These are the main functions the user should be using, unless they need
###some sort of customization
def initComsDriverAndEng(fileName=fname, logFunc=print):
	try:
		commands = pfunc.parseCommandData(fileName)
		driver = pfunc.createDriverInstance()
		engine = pfunc.createEngine()
	except:
		common.templatedExceptionPrint(e, "initComsDriverAndEng")

	#return a list instead of a tuple, as lists are iterable and mutable
	#Reason: while this is a helper function, we want to give some degree
	#of control over the returned data to promote customization where appropriate
	return [commands, driver, engine]

def execAllComs(commands, driver, engine, debug=False, logFunc=print):
	try:
		for cmd in commands:
			if(debug):
				logFunc("Parsing {}".format(str(cmd)))
			pfunc.execute(driver, engine, cmd)
	except Exception as e:
		common.templatedExceptionPrint(e, "execAllComs")

def executeBasicScript():
	execAllComs(*initComsDriverAndEng())
	