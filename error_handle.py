import traceback

def testError(var):

    try:
        newVar = int(var)
    except:
        trace = traceback.format_exc()
        print 'ERROR: ' + trace

def testZeroDiv(num1, num2):

    trace = False

    try:
        res = num1 / num2
    except ValueError:
        trace = traceback.format_exc()
##        print 'ValueError'
        print trace.splitlines()[-1]
        res = 0
    except ZeroDivisionError:
        trace = traceback.format_exc()
##        print 'ZeroDivisionError'
        print trace.splitlines()[-1]
        res = 0
    except TypeError:
        trace = traceback.format_exc()
##        print 'TypeError'
        print trace.splitlines()[-1]
        res = 0
    except:
        trace = traceback.format_exc()
        print 'Error not define'
        print trace.splitlines()[-1]
        res = 0
    else:
        print 'Very well, job done! No zero division.'

    if trace:
        print 'Please read the error message and try again.'

    return res

def testZeroDivWithRaise(num1, num2):

    try:
        res = num1 / num2
    except ValueError:
        trace = traceback.format_exc()
        print trace.splitlines()[-1]
        raise SystemExit
    except ZeroDivisionError:
        trace = traceback.format_exc()
        print trace.splitlines()[-1]
        raise SystemExit
    except TypeError:
        trace = traceback.format_exc()
        print trace.splitlines()[-1]
        raise SystemExit
    except:
        trace = traceback.format_exc()
        print 'Error not define'
        print trace.splitlines()[-1]
        raise SystemExit
    else:
        print 'Very well, job done! No zero division.'

    return res

class myError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def testmyError():

    try:
        int('a')

    except:
        er = myError(4)
        print 'My exception occurred, value:', er.value
        raise er
