
import matplotlib
matplotlib.use("WXAgg")
import wx
import datacollect
from threading import Thread,Lock
import numpy as N
import Queue

class PlotPanel(wx.Panel):
    
    def __init__(self,parent,yrange=(-3,3),**kwargs):
        from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
        from matplotlib.figure import Figure
        
        self.dw = DataWindow()
        
        # initialize Panel
        if 'style' not in kwargs.keys():
            kwargs['style'] = wx.NO_FULL_REPAINT_ON_RESIZE
        wx.Panel.__init__( self, parent, **kwargs )

        # initialize matplotlib stuff
        self.figure = Figure()
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure )
        
        self.subplot_x = self.figure.add_subplot(311)
        self.subplot_x.set_ylim(yrange)   
        self.subplot_x.set_xticks([])     
        self.subplot_y = self.figure.add_subplot(312)
        self.subplot_y.set_ylim(yrange) 
        self.subplot_y.set_xticks([])
        self.subplot_z = self.figure.add_subplot(313)
        self.subplot_z.set_ylim(yrange)
        self.subplot_z.set_xticks([])
        
        self.dw.winlock.acquire()
        self.line_x, = self.subplot_x.plot(self.dw.win[:,0],color='r',lw=2,animated=True)
        self.line_y, = self.subplot_y.plot(self.dw.win[:,1],color='g',lw=2,animated=True)
        self.line_z, = self.subplot_z.plot(self.dw.win[:,2],color='b',lw=2,animated=True)
        self.dw.winlock.release()
        self.canvas.draw()
        self.draw()
        
        self.dw.start()
                
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.OnTimer,self.timer)
        self.timer.Start(1)

    def OnTimer(self,event):
        self.draw()

    def draw( self ):
        """Draw data."""
        if not hasattr(self, 'background' ):
            self.background = self.canvas.copy_from_bbox(self.figure.bbox)
            
        self.canvas.restore_region(self.background)
        self.dw.winlock.acquire()
        self.line_x.set_ydata(self.dw.win[:,0])
        self.line_y.set_ydata(self.dw.win[:,1])
        self.line_z.set_ydata(self.dw.win[:,2])
        self.dw.winlock.release()
        
        self.subplot_x.draw_artist(self.line_x)
        self.subplot_y.draw_artist(self.line_y)
        self.subplot_z.draw_artist(self.line_z)
        
        self.canvas.blit(self.subplot_x.bbox)
        self.canvas.blit(self.subplot_y.bbox)
        self.canvas.blit(self.subplot_z.bbox)
        
        
class DataWindow(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.win = N.zeros((100,3))
        self.winlock = Lock()
    
    def run(self):
        self.dc = datacollect.DataCollector()
        self.dc.start()
        self.running = True
        while self.running:
            self.winlock.acquire()
            try:
                while 1:
                    newdata = self.dc.q.get(block=False)
                    self.win[:-1,:] = self.win[1:,:]
                    self.win[-1,:] = newdata
            except Queue.Empty:
                pass
            finally:
                self.winlock.release()
        self.dc.stop()
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    import optparse
    
    parser = optparse.OptionParser()
    parser.add_option("-y","--y",dest="yrange",help="Set the yrange",default=3,type="int")
    options,args = parser.parse_args()
    
    app = wx.PySimpleApp( 0 )
    frame = wx.Frame( None, title='WxPython and Matplotlib', size=(300,300) )
    panel = PlotPanel(frame,(-options.yrange,options.yrange))
    frame.Show()
    app.MainLoop()
