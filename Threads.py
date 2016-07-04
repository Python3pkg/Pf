THREADS = []

def startThread(t):
    THREADS.append(t)
    t.start()

def endThread(t):
    idx = THREADS.index(t)
    t.join()

def endALL():
    for t in THREADS:
        t.join()