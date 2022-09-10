import queue

q = queue.Queue()

def addTicker(item):
    q.put(item)

def getTicker():
    return q.get()

# class webSocketQueue:
#     def __init__(self):
#         self.q = queue.Queue()
#         pass

#     def addTicker(self, ticker):
#         self.q.put(ticker)

#     def getTicker(self):
#         return self.q.get()