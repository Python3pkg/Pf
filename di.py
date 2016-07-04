from easydict import EasyDict as edict
from collections import defaultdict
SPECIAL_TASK_NAMES = edict({
    "END":"END",
    "START":"START"
})


END = True
NOT_END = False

TASKS = []


def AddTask(name, lst):
    id = len(TASKS)
    TASKS.append(edict({
        'id':id,
        'chain':lst,
        'name': name
    }))
    TASK_ID[name] = id




SERVICES = {}
TASK_ID = {}

CACHE_DEPS = defaultdict(lambda:defaultdict(lambda: NOT_END))  #don't support task dependency yet, but keep the possibility

def Register(sKey, sFun):
    SERVICES[sKey] = sFun
def ParseTaskName(s):
    ## current no parsing
    if type(s) != str:
        r =  ParseTaskName(s[0])
        r.opt = s[1]
        return r


    if ":" not in s:
        return edict({'name':s,'deps':[],'opt':None})
    else:
        name, deps = s.split(":")
        result = edict({'name':name,'deps':[],'opt':None})
        deps = deps.split(",")
        for d in deps:
            if "." not in d:
                result.deps.append(edict({'name':d, 'task':SPECIAL_TASK_NAMES.END}))
            else:
                s1,s2 = d.split('.')
                result.deps.append(edict({'name':s1, 'task':s2}))
        return result

def TranslateStringChain(chain):
    return  [ParseTaskName(c)  for c in chain]



class Task:
    def __init__(self, id, name, dct):
        self.service = SERVICES[dct.name]
        self.prevT = None
        self.nextT = None
        self.id = id
        self.mainName = name
        self.subName = dct.name
        self.buff = None
        self.deps = dct.deps
        self.Opt = dct.opt
    def call(self, deps):
        return self.service(self.buff, deps, edict({'Opt':self.Opt, 'Name':self.mainName+'.'+self.subName, 'ID':self.id}))


def ToServiceChain(obj):
    r = [Task(obj.id, obj.name, c) for c in TranslateStringChain(obj.chain)]
    for i in range(len(r)):  ## build a linkedlist
        try:
            r[i].prevT = r[i-1]
            r[i].nextT = r[i+1]
        except IndexError:
            pass
    return r

def toServiceChains(chains):
    return [ToServiceChain(c) for c in chains]



def Clear(task_only=True):
    if not task_only:
        SERVICES.clear()
    TASK_ID.clear()
    CACHE_DEPS.clear()
    TASKS[:] = []