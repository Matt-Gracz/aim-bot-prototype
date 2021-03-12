#logging functions
##todo create more logging functions & specify log file
def printDebug(message):
    if(DEBUG):
        print("DEBUG: {}".format(message))

def templatedExceptionPrint(funcName, exception):
    tb = ''.join(traceback.format_tb(exception.__traceback__))
    exceptionMessage = "Exception: {}\nOccured at\n{}".format(str(exception), tb)
    logFunc("Something went wrong in {}}!\n{}".format(funcName, exceptionMessage))