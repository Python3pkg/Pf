from threading import Thread
import di
from Threads import *
import time


def ResumeTask(task):
    deps = []
    for d in task.deps:
        id = di.TASK_ID[d.name]
        subName = d.task
        while di.CACHE_DEPS[id][subName] == di.NOT_END:
            time.sleep(0.1)
        deps.append(di.CACHE_DEPS[id][subName])


    buff = task.call(deps)
    di.CACHE_DEPS[task.id][task.subName] = buff



    if task.nextT:
        task.nextT.buff = buff
        ResumeTask(task.nextT)
    else:
        di.CACHE_DEPS[task.id][di.SPECIAL_TASK_NAMES.END] = di.END



def Run():
    for t in di.toServiceChains(di.TASKS):
        startThread(Thread(target=ResumeTask, args=(t[0],)))
    endALL()