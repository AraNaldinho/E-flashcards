# This is a template for e-flashcard for Vidyasagar (Formerly called Spastic Society of India)
# Developed by Dr.Bama Srinivasan - bama@annauniv.edu, chorse@gmail.com
#------------------------------------------------------------------------------

import wx
import os
import wx.lib.agw.gradientbutton
import wx.lib.colourdb
import pyglet
from wx.lib.wordwrap import wordwrap

class MySplashScreen(wx.SplashScreen):
    """
Create a splash screen widget.
    """
    def __init__(self, parent=None):
        # This is a recipe to a the screen.
        # Modify the following variables as necessary.
        aBitmap = wx.Image(name = "splash.png").ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 1000 # milliseconds
        # Call the constructor with the above arguments in exactly the
        # following order.
        wx.SplashScreen.__init__(self, aBitmap, splashStyle,
                                 splashDuration, parent)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        wx.Yield()
#----------------------------------------------------------------------#

    def OnExit(self, evt):
        self.Hide()
        frame = eflashframe(None,-1,'E-flash cards')
        app.SetTopWindow(frame)        
        frame.Show(True)
        # The program will freeze without this line.
        evt.Skip()  # Make sure the default handler runs too...
#-----------------------------------------------------------------------#
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
        about_ico = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR, (16,16))
        aboutTool = self.toolbar.AddSimpleTool(wx.ID_ANY, about_ico, "About", "About E-flash card")
        self.Bind(wx.EVT_MENU, self.onAbout, aboutTool)
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
      
        
        
        #self.imageHolder.Bind(wx.EVT_LEFT_UP, self.onClick)
        #self.panel.Bind(wx.EVT_LEFT_UP,self.onClick)
        
        self.mainSizer.Add(self.imageHolder, 1, wx.CENTER, 5)
        font = wx.Font(32, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL)
        
        #################################################################################
        #Only two buttons, NEXT and EXIT are used. After checking with Vidyasagar, we may 
        #have to include PREVIOUS button also.
        ##################################################################################
        self.nxtbtn = wx.Button(self.panel,1, 'NEXT', (50,self.height - 200),(130,80)) 
        self.nxtbtn.SetFont(font)
        self.nxtbtn.SetBackgroundColour("yellow")
        self.nxtbtn.SetForegroundColour(wx.Colour(0,0,0))        
        self.xitbtn = wx.Button(self.panel,2,'EXIT',(self.width - 150,self.height-200),(110,80))
        self.xitbtn.SetFont(font)
        self.xitbtn.SetBackgroundColour("red")
        self.xitbtn.SetForegroundColour(wx.Colour(255,255,255))
        
        self.Bind(wx.EVT_BUTTON, self.onNext, id=1)
        self.Bind(wx.EVT_BUTTON, self.onClose, id=2)        
        
        self.SetSizer(self.mainSizer)   
        self.loadimg()
        self.bupdate() 
        #################################################################################
    def onAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "E-Flash card"
        info.Version = "1.0.0 Beta"
        info.Copyright = "(C) Department of IST, Anna University"
        info.Description = wordwrap(
        "This is an application for differently abled children and can be accessed through "
        "switch access scanning",
        350, wx.ClientDC(self.panel))
        #info.WebSite = ("http://www.pythonlibrary.org", "My Home Page")
        info.Developers = ["Bama Srinivasan", "Ranjani Parthasarathi","Voice: A.S Narayanan","Images from: http://animalphotos.info/a/","Peacock image: Thimindu Goonatillake from Colombo, Sri Lanka"]
        
        info.License = wordwrap("This program is free software: you can redistribute it and/or modify "
        "it under the terms of the GNU General Public License as published by "
        "the Free Software Foundation, either version 3 of the License, or "
        "(at your option) any later version. This program is distributed in the hope that it will be useful, "
        "but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A "
        "PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received "
         "a copy of the GNU General Public License along with this program. If not, see "
        "<http://www.gnu.org/licenses/>.",500, wx.ClientDC(self.panel))
        # Show the wx.AboutBox
        wx.AboutBox(info)
        
###############################################################       
      
    def bupdate(self): # First show the next button for 5 seconds
            self.nxtbtn.Show()
            self.xitbtn.Hide()
        ##############################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by clicking on to the screen
        #########################################################################################
            self.imageHolder.Bind(wx.EVT_LEFT_UP, self.onNext)
            self.panel.Bind(wx.EVT_LEFT_UP,self.onNext)
            wx.CallLater(5000,self.xshow) #5000 - 5 seconds

    def xshow(self): # Alternate xit button for the next five seconds
        self.nxtbtn.Hide ()
        self.xitbtn.Show()
        ##############################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by clicking on to the screen
        #########################################################################################
        self.imageHolder.Bind(wx.EVT_LEFT_UP, self.onClose)
        self.panel.Bind(wx.EVT_LEFT_UP,self.onClose)
        wx.CallLater(5000,self.bupdate)
                         
    
###############################################################################
    def loadimg(self):        
        self.pictureCount = len(self.listimg)       
        self.displayImage(self.listimg[0])        
        
###############################################################################
    def OnSound(self,image):
        filename,extension = os.path.splitext(image)
        firstimage = filename[8:]  # Remove 'animal/' and extract only the file name      
          
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
###############################################################################   
       

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

###############################################################################        
        
    def nextImage(self):
        if self.pictureIndex == self.pictureCount-1:
            self.pictureIndex = 0
        else:
            self.pictureIndex += 1
        print self.listimg[self.pictureIndex]
        self.displayImage(self.listimg[self.pictureIndex])      
        
        
    #######################################################################
    def onNext(self, event):
        self.nextImage()
    #######################################################################
    def onClose(self,event):
        self.Close()
    ######################################################################
    
 ###############################################################################       
            
                    
class MyApp(wx.App):
    def OnInit (self):
        MySplash = MySplashScreen()
        MySplash.Show()
        
        return True
    
app = MyApp (0)
app.MainLoop()
