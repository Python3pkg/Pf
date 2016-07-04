from __init__ import *
import time

def echo(buff, deps, meta):
    print "In the {0} (thread {1})".format(meta.Name, meta.ID)
    print meta.Opt, meta.ID
    return END


def echo_prev(buff, deps, meta):
    print "In the {0} (thread {1})".format(meta.Name, meta.ID)
    print buff, deps, meta.ID
    return END

def sleep(buff, deps, meta):
    time.sleep(10)
    return END


Register("Echo", echo)
Register("EchoP", echo_prev)
Register("Sleep", sleep)
AddTask("T1", ["Echo", "Echo"])
AddTask("TT", ["Echo", "EchoP"])
Run()

Clear()

AddTask("T1",["Sleep"])
AddTask("T2", [["Echo", "helloworld"], "EchoP"])
AddTask("TFinal", ["Echo:T1", ["Echo:T2.Echo", "end"]])

#
#
Run()