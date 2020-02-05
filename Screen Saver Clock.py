from math import sin, cos, pi
from threading import Thread

from tkinter import Tk,Canvas,Label     

from datetime import datetime

class mapper:
    def __init__(self, world, viewport):
        self.world = world 
        self.viewport = viewport
        x_min, y_min, x_max, y_max = self.world
        X_min, Y_min, X_max, Y_max = self.viewport
        f_x = float(X_max-X_min) / float(x_max-x_min) 
        f_y = float(Y_max-Y_min) / float(y_max-y_min) 
        self.f = min(f_x,f_y)
        x_c = 0.5 * (x_min + x_max)
        y_c = 0.5 * (y_min + y_max)
        X_c = 0.5 * (X_min + X_max)
        Y_c = 0.5 * (Y_min + Y_max)
        self.c_1 = X_c - self.f * x_c
        self.c_2 = Y_c - self.f * y_c

    def __windowToViewport(self, x, y):
        X = self.f *  x + self.c_1
        Y = self.f * -y + self.c_2      
        return X , Y

    def windowToViewport(self,x1,y1,x2,y2):
        return self.__windowToViewport(x1,y1),self.__windowToViewport(x2,y2)
class makeThread (Thread):
      def __init__ (self,func):
          Thread.__init__(self)
          self.__action = func
          self.debug = False

      def __del__ (self):
          if ( self.debug ): print ("Thread end")

      def run (self):
          if ( self.debug ): print ("Thread begin")
          self.__action()
class clock:
    def __init__(self,root,deltahours = 0,sImage = True,w = 400,h = 400,useThread = False):
        self.world       = [-1,-1,1,1]

        self.showImage = False

        self.setColors()
        self.circlesize  = 0.09
        self._ALL        = 'handles'
        self.root        = root
        width, height    = w, h
        self.pad         = width/16


        self.canvas = Canvas(root, width = width, height = height, background = self.bgcolor, border=0)
        viewport = (self.pad,self.pad,width-self.pad,height-self.pad)
        self.T = mapper(self.world,viewport)

        self.canvas.bind("<Configure>",self.resize)
        self.canvas.pack(fill='both', expand='yes')

        if useThread:
           st=makeThread(self.poll)
           st.debug = True
           st.start()
        else:
           self.poll()

        self.label=Label(self.canvas,text='@ TD',bg='black',fg='blue')
        self.label.place(relx=0.01,rely=0.96)
           
    def resize(self,event):
        sc = self.canvas
        sc.delete('all')            
        width  = sc.winfo_width()
        height = sc.winfo_height()

        imgSize = min(width, height)
        self.pad = imgSize/16
        viewport = (self.pad,self.pad,width-self.pad,height-self.pad)
        self.T = mapper(self.world,viewport)

        self.canvas.create_rectangle([[0,0],[width,height]], fill = self.bgcolor)

        self.redraw()             

    def setColors(self):
       self.bgcolor     = 'black'
       self.timecolor   = 'white'
       self.circlecolor = 'blue'

    def redraw(self):
        start = pi/2              # 12h is at pi/2
        step = pi/6
        for i in range(12):       # draw the minute ticks as circles
            angle =  start-i*step
            x, y = cos(angle),sin(angle)
            self.paintcircle(x,y)
        self.painthms()           # draw the handles
        if not self.showImage:
           self.paintcircle(0,0)  # draw a circle at the centre of the clock
        
   
    def painthms(self):
        self.canvas.delete(self._ALL)  # delete the handles
        
        T=datetime.now().time()
        h=T.hour
        m=T.minute
        s=T.second
        
    
        angle = pi/2 - pi/6 * (h + m/60.0)
        x, y = cos(angle)*0.70,sin(angle)*0.70   
        scl = self.canvas.create_line
        # draw the hour handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, width = self.pad/3)
        angle = pi/2 - pi/30 * (m + s/60.0)
        x, y = cos(angle)*0.90,sin(angle)*0.90
        # draw the minute handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, width = self.pad/5)
        angle = pi/2 - pi/30 * s
        x, y = cos(angle)*0.95,sin(angle)*0.95   
        # draw the second handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, arrow = 'last')

    def paintcircle(self,x,y):
        ss = self.circlesize / 2.0
        sco = self.canvas.create_oval
        sco(self.T.windowToViewport(-ss+x,-ss+y,ss+x,ss+y), fill = self.circlecolor)
  
    def poll(self):
        self.redraw()
        self.root.after(200,self.poll)

def Exit(event):
    root.destroy()
    exit()

root = Tk()
root.state('zoomed')
root.overrideredirect(True)

root.bind_all('<Any-KeyPress>',Exit)
root.bind_all('<Any-Button>',Exit)
root.bind_all('<Motion>',Exit)

clock(root)


root.mainloop()

