# This is a template for e-flashcard for Vidyasagar (Formerly called Spastic Society of India)
# Developed by Dr.Bama Srinivasan - bama@annauniv.edu, chorse@gmail.com
#------------------------------------------------------------------------------

import wx
import os
import wx.lib.agw.gradientbutton
import wx.lib.colourdb
import pyglet
import random
import dircache

class eflashframe(wx.Frame):
    def __init__(self,parent,id,title):
        self.frame = wx.Frame.__init__(self,parent,id, title, pos = (0,0),size = wx.DisplaySize()) # for full screen
        #self.frame = wx.Frame.__init__(self,parent,id,title,pos=(10,10),size = (800,600))
        self.SetBackgroundColour(wx.BLACK)
        self.panel = wx.Panel(self)   
        self.panel.SetBackgroundColour(wx.BLACK)
        self.folderPath = ""
        #self.pictureCount = 0 
        self.pictureIndex = 0
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.PhotoMaxSize = 900
        ############################################################################################
        #Create tool bar for Open directory alone. All the images are to be stored in this directory
        ############################################################################################
        self.toolbar = self.CreateToolBar()
        #self.toolbar.SetToolBitmapSize((16,16))
        #open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
        #openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Folder")
        #self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)
        self.toolbar.Realize()
        self.listimg = []
        animals = os.listdir('animals')
        sound = os.listdir('sound')
        for root,dir,files in os.walk('animals'):
            for animal in animals:
                self.listimg.append(os.path.join(root,animal))   
        self.soundlist = []
        for name in sound:
            filename,extension = os.path.splitext(name)
            self.soundlist.append(filename)   
        self.width, self.height = wx.DisplaySize()     
        starterImage = wx.EmptyImage(self.width,self.height)
        self.imageHolder = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(starterImage))
      
        
        #########################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by clicking on to the screen
        #########################################################################################
        self.imageHolder.Bind(wx.EVT_LEFT_UP, self.onClick)
        self.panel.Bind(wx.EVT_LEFT_UP,self.onClick)
        
        self.mainSizer.Add(self.imageHolder, 1, wx.CENTER, 5)
        font = wx.Font(28, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        #################################################################################
        #Only two buttons, NEXT and EXIT are used. After checking with Vidyasagar, we may 
        #have to include PREVIOUS button also.
        ##################################################################################
        self.nxtbtn = wx.ToggleButton(self.panel,1, 'NEXT', (50,self.height - 200),(110,80)) 
        self.nxtbtn.SetFont(font)
        self.nxtbtn.SetBackgroundColour(wx.RED)
        self.nxtbtn.SetForegroundColour(wx.BLACK)
        self.xitbtn = wx.ToggleButton(self.panel,2,'EXIT',(self.width - 150,self.height-200),(110,80))
        self.xitbtn.SetFont(font)
        self.xitbtn.SetBackgroundColour(wx.RED)
        self.xitbtn.SetForegroundColour(wx.BLACK)
        
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onNext, id=1)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onClose, id=2)
        
        #Toggle button is used, so that the scan timings can be adjusted easily.
        self.SetSizer(self.mainSizer)   
        self.loadimg()
        # This function is for scanning with time frame of three seconds.
        self.update() 
        
###############################################################   
     
    def update(self):        
        xit = self.xitbtn.GetValue()
        nxt = self.nxtbtn.GetValue()
        if nxt == False:
            self.nxtbtn.SetValue(True)
            self.nxtbtn.Show()
            self.xitbtn.SetValue(False)
            self.xitbtn.Hide()
            self.nxtbtn.SetBackgroundColour(wx.GREEN)
            self.nxtbtn.SetLabel("NEXT")
            self.xitbtn.SetBackgroundColour(wx.RED)
            
        elif nxt == True:
            self.nxtbtn.SetValue(False)  
            self.nxtbtn.Hide()                
            self.xitbtn.SetValue(True)
            self.xitbtn.Show()
            self.nxtbtn.SetBackgroundColour(wx.RED)       
            self.xitbtn.SetBackgroundColour(wx.GREEN)
        #print 'nxt',nxt
        wx.CallLater(3000,self.update)#3000-3 seconds.       
        
    
###############################################################################
    def loadimg(self):
        #print self.listimg
        #print self.images
        #print self.soundlist
        self.pictureCount = len(self.listimg)
        #print self.pictureCount
        #self.displayImage('monkey')
        self.displayImage(self.listimg[0])        
        
###############################################################################
    def OnSound(self,image):
        filename,extension = os.path.splitext(image)
        firstimage = filename[8:]  # Remove animal/ and extract only the file name      
          
        print firstimage
        for snd in self.soundlist:            
            if firstimage == snd:
                animal = 'sound/'+snd+'.mp3'
                music = pyglet.media.load(animal)
                music.play()
                def exiter(dt):
                    pyglet.app.exit()
                pyglet.clock.schedule_once(exiter,music.duration)
                pyglet.app.run() 
                    
   
           
        #print self.pictureCount
        #print self.pictureIndex

    def displayImage(self,image):                
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)        
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)            
        self.imageHolder.SetBitmap(wx.BitmapFromImage(img))          
        self.mainSizer.Layout()
        self.panel.Center() 
        self.Center()
        self.Refresh()  
        wx.FutureCall(1000, self.OnSound,image) 

        
        
    def nextImage(self):
        if self.pictureIndex == self.pictureCount-1:
            self.pictureIndex = 0
        else:
            self.pictureIndex += 1
        print self.listimg[self.pictureIndex]
        self.displayImage(self.listimg[self.pictureIndex])      
        
        
    #######################################################################
    def onNext(self, event):
        nxt = self.nxtbtn.GetValue()
        print nxt
        if nxt == True:
            self.nextImage()
    #######################################################################
    def onClose(self,event):
        xit = self.xitbtn.GetValue()
        print xit
        if xit == True:
            self.Close()
    ######################################################################
    def onClick(self,event):
        nxt = self.nxtbtn.GetValue()
        xit = self.xitbtn.GetValue()
        print nxt, xit
        if nxt == True:
            self.nextImage() 
        if xit == True:
            self.Close()
            
                    
class MyApp(wx.App):
    def OnInit (self):
        frame = eflashframe(None,-1,'E-flash cards')
        frame.Show(True)
        return True
    
app = MyApp (0)
app.MainLoop()
