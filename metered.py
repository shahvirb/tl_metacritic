import Queue
import time

class Meter:
    def __init__(self, interval):
        self.interval = interval
        self.runq = Queue.Queue()
        self.prev = self.set_prev_now()
    
    def set_prev_now(self):
        self.prev = time.time()
    
    def run(self, fn, *args):
        self.runq.put((fn, args))
        
    def work(self):
        if not self.runq.empty() and (time.time() - self.prev >= self.interval):
            fn, args = self.runq.get()
            fn(*args)
            self.prev = time.time()
            
    def timed_out(self, timeout):
        return True if time.time() - self.prev >= timeout else False

def main():
    def print_fn(a, b):
        print(a, b)
    
    meter = Meter(1)
    for i in range(3):
        meter.run(print_fn, 'i = ', i)
    while True:
        meter.work()

if __name__ == '__main__':
    main()