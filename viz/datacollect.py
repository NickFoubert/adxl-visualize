import serial
import time
from threading import Thread
import Queue

class DataAdapter(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.q = Queue.Queue()
        self.running = False
    
    def stop(self):
        self.running = False

class ArduinoCollector(DataAdapter):        
    def run(self):
        ser = serial.Serial('/dev/tty.usbserial-11FP0105',9600,timeout=1)

        self.running = True
        while self.running:
            input = ser.readline()
            try:
                data = [float(x) for x in input.strip().split(',')]
            except:
                continue
            print input.strip()
            self.q.put(data)
        ser.close()
        
class FileCollector(DataAdapter):
    def __init__(self,filename,samplerate=10):
        DataAdapter.__init__(self)
        self.fn = filename
        self.sampleperiod = 1.0 / float(samplerate)
        fh = open(self.fn)
        lines = fh.readlines()
        fh.close()
        self.data = [map(float,x.strip().split(',')) for x in lines]
        self.lastsample = 0.0
    
    def run(self):
        self.running = True
        idx = 0
        while self.running:
            if time.time() - self.lastsample < self.sampleperiod:
                continue
            self.q.put(self.data[idx])
            idx = (idx + 1) % len(self.data)
            self.lastsample = time.time()
        self.running = False

if __name__ == "__main__":
    import signal

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

    
