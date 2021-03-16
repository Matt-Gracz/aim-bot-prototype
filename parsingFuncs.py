import chromedriver_binary #mgracz: I seem to need this to work with anaconda :-/ todo figure out how to remove this dependency
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas
from time import sleep
from sys import argv, stderr
import traceback
import constants
import commonObjsAndFuncs as common

###todo: meta-program this junk away in a dedicated class
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

"""
    A bit of additional explanation is warranted for the two different command-parsing funcs.
    
    The first func is intended to parse a spreadsheet of data rows, with each datum in each
    row corresponding to the column header, which is the name of the HTML element in which
    to input that datum.  A typical use case would be if you've got a big spreadsheet of,
    say, 1000 inventory items to add.  Then each row would be an inventory item, and each
    datum in that row would be a value for an HTML element (typically a text box).  The
    output would be a "Type El_i datum" command, where the total number of commands would
    be (#rows * #cols) in the input spreadsheet.  The user then can take this and buttress
    it with their own commands and run it through the second function

    The second func is intended to parse a list of commands, again in spreadsheet form, but
    this time the data all live in the right-most "Data" column and the preceding two columns
    specify the command and HTML element associated with each datum.

    TODO: Make the first function friendly to outputting to excel for obvious reasons

"""


#command-parsing functions
##parse excel file
"""File Format: 

    numCols = c, numRows = r

    htmlEl_0, htmlEl_1, ..., htmlEl_c
    0_val_0,  0_val_1,  ..., 0_val_c
    1_val_0,  1_val_1,  ..., 1_val_c
    ...
    r_val_0,  r_val__1, ..., r_val_c

#parsedData[i][0] = HTML element name for column i
#parsedData[i][1] = list of data for column i
#therefore parsedData[i][1][j] is the value of column i for data row j
#therefore row j = [parsedData[i][1][j] for i in range(0,numCols)]

This function returns cmds that the engine can consume, where a row's format is: 

    [ ["Type", htmlEl_0, 0_val_row], ... ["Type", htmlEl_j, j_val_row] ]

    i.e., each element of cmd is the full set of input commands for one data row
    in the excel sheet provided by fileName.

This ends up being a 3D list, characterized by the following order of indeces:
    cmds[elementIndex] = a single data element in AiM, such as an inventory item or 
                         an asset

    cmds[elementIndex][commandIndex] = the command information for a piece of the 
                         data element at elementIndex, where "command" conforms to
                         the paradigm of commands consumed by the engine, for the
                         element and command specificed by elementIndex and commandIndex

    cmds[elementIndex][commandIndex][commandPieceindex] = a piece of the
                        [action,HTML element, data] style command consumed by the engine

"""
def parseUserInputData(fileName=fname, numRows=None, formName=""):
    dataFile = pandas.read_excel(fileName)
    parsedData = [_ for _ in dataFile.items()]
    htmlEls = [formName+parsedData[i][0] for i in range(0,len(parsedData))]
    numCols = len(parsedData)
    if(not numRows):
        numRows = len(parsedData[1][1])
    rows = [[parsedData[i][1][j] for i in range(0,numCols)] for j in range(0,numRows)]
    cmds = [[["Type", htmlEls[i], str(row[i])] for i in range(0,numCols)] for row in rows]
    return cmds


##parse pre-configured excel sheet of commands where the columns and rows are like so:
##
## command           HTML element           data
##  type               username            jdoe@university.edu
## click               password            
##  type               password             itsAsecret123
def parseCommandData(fileName=fname):
    parsedCommandData = [_ for _ in read_excel(fileName).items()]
    pcd = parsedCommandData #shorten name for readability in the list comp below
    ###Note: pcd[0]=user actions, pcd[1]=HTML element IDs, pcd[2]=textual data
    return [_ for _ in zip(*[pcd[i][1] for i in range(0,3)])]

#Write the output of parseCommandData to an excel sheet for review, tweaking, and/or
#buttressing of the commands to be executed.  Returns True iff successful
def parseCommandDataToExcel(commandFileName=fname, outputFileName=defaultOutputFileName):
    try:
        pcd = parseCommandData(fileName)
        #from 3D to 2D, necessary for exporting coherently to a single 2D excel spreadsheet
        pcdFlat = [cmd for element in pcd for cmd in element] 
        pcdFlatDataFrame = pandas.DataFram.from_records(pcdFlat)
        #IMPORTANT:
        #header and index are just the col and row labels, which are just 0-indexed indeces,
        #and therefore not only are useless but would cause errors when actually trying to
        #execute commands.  Theerfore header and index are both False, and *NEED* to be
        pcdFlatDataFrame.to_excel(outputFileName, header=False, index=False)
        return True
    except Exception as e:
        common.logError("Something went wrong in parseCommandDataToExcel", e)
        return False

def createDriverInstance(startUrl = None):
    driver = webdriver.Chrome()
    driver.get(url if startUrl is None else startUrl)
    ###todo: make this the beginning of the config GUI?  Seems wrong...
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