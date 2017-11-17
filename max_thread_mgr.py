import threading
import Queue
import time

class Manager:
    def __init__(self, max=16):
        self.thread_q = Queue.Queue()
        self.run_q = Queue.Queue(maxsize=max)
    
    def start_threads(self):
        self.wait_free()
        while not self.run_q.full():
            t = self.thread_q.get()
            self.run_q.put(t)
            t.start()
    
    def on_thread_finished(self):
        pass
    
    def add_thread(self, t):
        self.thread_q.put(t)
        #self.start_threads()
        
    def wait_free(self):
        while self.run_q.full():
            time.sleep(0)
            
    def join(self):
        while not self.thread_q.empty():
            self.start_threads()