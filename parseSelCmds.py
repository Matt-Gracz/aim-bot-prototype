import chromedriver_binary #seem to need this to work with anaconda :-/ todo figure out how to remove this dependency
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import read_excel
from enum import Enum
from time import sleep
from sys import argv, stderr

#todo: design issues to address - lack of OOP, global variables dangling everywhere, messy command init structure,
#                                 debugging is weird, data format validation, implement python package guidelines,
#                                 and there might be performance scalability issues for lots of data; it takes
#                                 ~10 minutes to enter in ~100 data points of inventory for example.

#constants
##todo: turn these into cli args
waitIntervalInSecs = .75
explicitWaitInSecs = 5
url = "http://127.0.0.1:8080/fmax/screen/WORKDESK"
fname = 'test-excel-file.xlsx'
DEBUG = False

#logging functions
##todo create more logging functions & specify log file
def printDebug(message):
	if(DEBUG):
		print("DEBUG: {}".format(message))

#helper funcs
##getter-setters for module consts
###todo: meta-program this junk away in a dedicated class
# def getSetWaitInterval(newWI = None):
# 	waitIntervalInSecs = newWI if newWI is not None else waitIntervalInSecs
# 	return waitIntervalInSecs
# def getSetExplicitWait(newEW = None):
# 	explicitWaitInSecs = newEW if newEW is not None else explicitWaitInSecs
# 	return waitIntervalInSecs
# def getSetUrl(newURL = None):
# 	url = newURL if newURL is not None else url
# 	return url
# def getSetFileName(newFN = None):
# 	fname = newFN if newFN is not None else fname
# 	return fname
# def getSetDebugLevel(newDL = None):
# 	DEBUG = newDL if not newDL is not None else DEBUG
# 	return DEBUG

##parse excel file
"""File Format: 

	numCols = c, numRows = r

	htmlEl_0, htmlEl_1, ..., htmlEl_c
	0_val_0,  0_val_1,  ..., 0_val_c
	1_val_0,  1_val_1,  ..., 1_val_c
	...
	r_val_0,  r_val__1, ..., r_val_c

#parsedData[i][0] = HTML element for column i
#parsedData[i][1] = list of data for column i
#therefore parsedData[i][1][j] is the value of column i for data row j
#therefore row j = [parsedData[i][1][j] for i in range(0,numCols)]

This function returns cmds that the engine can consume, where a row's format is: 

	[ ("Type", htmlEl_0, 0_val_row), ... ("Type", htmlEl_j, j_val_row) ]

	i.e., each element of cmd is the full set of input commands for one data row
	in the excel sheet provided by fileName.
"""
def parseUserInputData(fileName=None, numRows=None, formName=""):
	if(not fileName):
		fileName = fname
	dataFile = read_excel(fileName)
	parsedData = [_ for _ in dataFile.items()]
	htmlEls = [formName+parsedData[i][0] for i in range(0,len(parsedData))]
	numCols = len(parsedData)
	if(not numRows):
		numRows = len(parsedData[1][1])
	rows = [[parsedData[i][1][j] for i in range(0,numCols)] for j in range(0,numRows)]
	cmds = [[["Type", htmlEls[i], str(row[i])] for i in range(0,numCols)] for row in rows]
	return cmds

##other helpers
def parseCommandData(fileName=None):
	if(not fileName):
		fileName = fname
	parsedCommandData = [_ for _ in read_excel(fileName).items()]
	pcd = parsedCommandData #shorten name for readability
	###Note: pcd[0]=user actions, [1]=Website element IDs, [2]=textual data
	return [_ for _ in zip(*[pcd[i][1] for i in range(0,3)])]

def createDriverInstance(startUrl = None):
	driver = webdriver.Chrome()
	driver.get(url if startUrl is None else startUrl)
	###todo: make this the beginning of the GUI
	input("Please log in and then press any key to continue.")
	return driver

#engine
##engine functions
###data-sensitive functions
def sendKeysToEl(element, data):
	element.send_keys(data)

###data-ignorant functions
def clickEl(element, data=None):
	element.click()

def sendTabToEl(element, data=None):
	element.send_keys(Keys.TAB)

def clearEl(element, data=None):
	element.clear()

###main engine functions
def execute(driver, engine, cmd):
	sleep(waitIntervalInSecs)
	print("Preparing to execute {}".format(cmd))
	element = WebDriverWait(driver, explicitWaitInSecs).until(EC.visibility_of_element_located((By.ID, cmd[1])))
	engine[cmd[0]](element, data=str(cmd[2]))

####todo: decouple name dependency with excel metadata for command types
def createEngine():
	return {'Type':sendKeysToEl, 'Click':clickEl, 'Tab':sendTabToEl, 'Clear':clearEl}

#script start
if __name__ == "__main__":
	try:
		##todo: create multi-level logging system
		##todo: make this parsing somewhat not horrid
		index = 2 if "python" in argv[0] else 1
		DEBUG = bool(argv[index])
	except:
		DEBUG = False
	print("DEBUG Level set to:  {}".format(DEBUG))
	##todo: pipe stderr to log file, also why doesn't this work?
	stderr = open('devnull', 'w')

	commands = parseCommandData()
	driver = createDriverInstance()
	engine = createEngine()
	for cmd in commands:
		printDebug("Parsing {}".format(str(cmd)))
		execute(driver, engine, cmd)
	print("Selenium Commands Completed")
	sleep(waitIntervalInSecs * 5)
	driver.close()
	print("Driver closed - exiting program")


