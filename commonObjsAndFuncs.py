import traceback
import datetime
import constants

## If this file gets unwieldy, consider breaking logging out into its own lib
## --mgracz

# ********************** LOGGING ********************** #
sharedLogFileName = "AiMBotLog.txt"

#"constant" level switch for differential message logging
class loggingLevels():
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
levels = loggingLevels()

# Nobody has a reason to invoke this, unless you're using it as callback or
# in some other weird situation.  If so, create a wrapper/getter function,
# please.  Something named like call/getPrivateLogGenericFunction.
# Thanks,
# --mgracz
def _logGenericMessage(message, level):
    with open(sharedLogFileName,"a") as logFile:
        timestamp = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
        logFile.write("{}, {}, {}\n".format(timestamp, level, message))

def createExceptionTracebackMessage(exception):
    tb = ''.join(traceback.format_tb(exception.__traceback__))
    tracebackMessage = "Exception: {} occured at:\n{}".format(str(exception), tb)
    return tracebackMessage

def logError(message=None, exception=None):
    if(message is not None):
        _logGenericMessage(message, levels.ERROR)
    if(exception is not None):
        tracebackMessage = createExceptionTracebackMessage(exception)
        _logGenericMessage(tracebackMessage, levels.ERROR)
def logInfo(message):
    _logGenericMessage(message, levels.INFO)
def logDebug(message):
    if(common.DEBUG):
        _logGenericMessage(message, levels.DEBUG)
def clearLog():
    open(sharedLogFileName,"w").close()