import serial
import time
from threading import Thread
import Queue
import signal

class DataCollector(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.q = Queue.Queue()
        
    def run(self):
        ser = serial.Serial('/dev/tty.usbserial-11FP0105',9600,timeout=1)
        
        self.running = True
        while self.running:
            input = ser.readline()
            try:
                data = [int(x) for x in input.strip().split(',')]
            except:
                continue
            self.q.put(data)
        
        ser.close()
        
    def stop(self):
        self.running = False

if __name__ == "__main__":
    
    running = True
    dc = DataCollector()
    
    def stop(signum,sf):
        global running
        running = False
        
    signal.signal(signal.SIGINT,stop)
    
    def printData():
        while running:
            try:
                print dc.q.get(timeout=1)
            except Queue.Empty:
                pass
    
    t = Thread(target=printData)
    t.start()
    dc.start()
    
    while running:
        pass
        
    dc.stop()

    