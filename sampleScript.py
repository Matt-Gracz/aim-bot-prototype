#script start
if __name__ == "__main__":
    try:
        ##todo: create multi-level logging system
        ##todo: make this parsing somewhat not horrid
        ##todo: stop putting todos in the comments :-/
        index = 2 if "python" in argv[0] else 1
        DEBUG = bool(argv[index])
    except:
        DEBUG = False
    print("DEBUG Level set to:  {}".format(DEBUG))
    ##todo: pipe stderr to log file, also why doesn't this work?
    stderr = open('devnull', 'w')

    #start sample script.  Users of the program shouldn't have to mess with the stuff above,
    #which is an intentional architectural decision, such that the below script is super
    #duper simple.  That way AiM IT folks don't need to know how selenium works, nor any
    #of the attendant thorny details

    executeBasicScript()
    print("Selenium Commands Completed")
    sleep(waitIntervalInSecs * 5)
    driver.close()
    print("Driver closed - exiting program")