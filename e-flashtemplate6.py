import wx
import os
import wx.lib.agw.gradientbutton
import wx.lib.colourdb
import pyglet
from wx.lib.wordwrap import wordwrap
from Tkinter import Tk
from tkFileDialog import askopenfilename
from os.path import exists, join
from os import pathsep
import string
#!/usr/bin/python
#------------------------------------------------------------------------------
# Search the file called "sample1.py" which is residing in the search_path
#variable and returning back 
#-------------------------------------------------------------------------------
#creating a window
class MySplashScreen(wx.SplashScreen):
    def __init__(self, parent=None):
        # This is a recipe to a the screen.
        # Modify the following variables as necessary.
        aBitmap = wx.Image(name = "splash.png").ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 1000 # milliseconds
        # Call the constructor with the above arguments in exactly the
        # following order.
        wx.SplashScreen.__init__(self, aBitmap, splashStyle,splashDuration, parent)
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
			self.nxtbtn.SetBackgroundColour("red")
			self.xitbtn.SetBackgroundColour("yellow")
			self.nxtbtn.Show()
			self.xitbtn.Show()
        ##############################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by clicking on to the screen
        #########################################################################################
			self.imageHolder.Bind(wx.EVT_LEFT_UP, self.onNext)
			self.panel.Bind(wx.EVT_LEFT_UP,self.onNext)
			wx.CallLater(5000,self.xshow) #5000 - 5 seconds

    def xshow(self): # Alternate xit button for the next five seconds
		self.nxtbtn.SetBackgroundColour("yellow")
		self.xitbtn.SetBackgroundColour("red")
		self.nxtbtn.Show()
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
          
        print (firstimage)
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
        print (self.listimg[self.pictureIndex])
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
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "INSERT", size=(400,600),pos=wx.DefaultPosition)
        panel = wx.Panel(self, -1) 
	panel.SetBackgroundColour("BLACK")       
        wx.StaticText(self, -1, "Name:", pos=(15, 20))
        self.textCtrl = wx.TextCtrl(self, -1, "", pos=(100, 20),)
 
        getPicture = wx.Button(self, label = "Get Picture", pos = (50,100),size=(250,100))
	getPicture.SetBackgroundColour("orange")
        getSound = wx.Button(self,label = "Get Sound", pos = (50,250),size=(250,100))
	getSound.SetBackgroundColour("orange")
        self.Bind(wx.EVT_BUTTON, self.OnGetPicture, getPicture)
        self.Bind(wx.EVT_BUTTON, self.OnGetSound, getSound)
        okButton = wx.Button(self,label="OK",pos = (75,400))
	okButton.SetBackgroundColour("green")
        self.Bind(wx.EVT_BUTTON, self.onReplace,okButton)
        cancelButton = wx.Button(self,label="Cancel",pos = (200,400))
	cancelButton.SetBackgroundColour("green")
        self.Bind(wx.EVT_BUTTON, self.onCancel,cancelButton)
    
    def onCancel(self,event):
        self.Close(True)
        #This function is for copying the file to the folder
    def OnGetSound(self,event):
        global copycmd, src, dest2, nsound, txt
        dlg = wx.FileDialog(self, message="Open an Audio...", defaultDir=os.getcwd(),defaultFile="", style=wx.OPEN)
        if dlg.ShowModal () == wx.ID_OK:
            picture=dlg.GetPath()
            nsound = dlg.GetFilename ()                       
            src = picture                        
        dlg.Destroy()
        dest2 = "sound"
        txt = nsound[-3:]        
        copycmd =  "copy " + picture + " "+ dest2 # copy the file in the folder
        print (copycmd)               
        os.system(copycmd)
        box=wx.MessageDialog(None,"sound are inserted","Deleted",wx.OK)
        box.ShowModal()
        box.Destroy()
	
    def OnGetPicture(self,event):
        global copycmd, src, dest1, npicture, txt1
        dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(),defaultFile="", style=wx.OPEN)
        if dlg.ShowModal () == wx.ID_OK:
            picture=dlg.GetPath()
            npicture = dlg.GetFilename ()                       
            src = picture                        
        dlg.Destroy()
        dest1 = "animals"
        txt1 = npicture[-3:]        
        copycmd =  "copy " + picture + " "+ dest1 # copy the file in the folder
        print (copycmd)               
        os.system(copycmd)
        box=wx.MessageDialog(None,"Image are inserted","Deleted",wx.OK)
        box.ShowModal()
        box.Destroy()
        
     # This function is for renaming the file after copying   
    def onReplace(self,event):
        global npicture, txt, nsound , txt1 ,dest1 ,dest2   
        namein = self.textCtrl.GetValue()
        givenName = namein +"." + txt1 
        print (givenName)
        dirs = os.listdir(dest1)
        if npicture in dirs:
			print ("found here")
			#a=str("animals\")
			#print (a)
			#a=str(a)+"animals/"
			renameCommand = "move "+"animals\\"+npicture+" "+'animals\\'+givenName
			print (renameCommand)                        
			os.system(renameCommand)
        namein = self.textCtrl.GetValue()
        givenName = namein +"." + txt 
        print (givenName)
        dirs = os.listdir(dest2)
        if nsound in dirs:
			#b=str("sound\")
			#b=str(b)+"sound/"
			print ("found here")
			renameCommand = "move "+"sound\\"+nsound+ " "+"sound\\"+givenName
			print (renameCommand)
			os.system(renameCommand)
        box=wx.MessageDialog(None,"Image and sound are inserted","INSERT",wx.OK)
        box.ShowModal()
        box.Destroy()
        self.Close(True)
class MyFrame1(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "DELETE", size=(400,600),pos=wx.DefaultPosition)
        panel = wx.Panel(self,-1)
        wx.StaticText(self, -1, "Name:", pos=(15, 20))
	font = wx.Font(32, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL)
        self.textCtrl = wx.TextCtrl(self, -1, "", pos=(100, 20))
        deletePicture = wx.Button(self, label = "Delete Picture", pos = (50,100),size=(250,100))
        deleteSound = wx.Button(self,label = "Delete Sound", pos = (50,250),size=(250,100))
        self.Bind(wx.EVT_BUTTON, self.OnDeletePicture, deletePicture)
	deletePicture.SetBackgroundColour("orange")
	deleteSound.SetBackgroundColour("orange")
        self.Bind(wx.EVT_BUTTON, self.OnDeleteSound, deleteSound)
        delete = wx.Button(self,label="Delete",pos = (75,400))
	delete.SetBackgroundColour("green")
        self.Bind(wx.EVT_BUTTON, self.OnDelete,delete)
        cancelButton = wx.Button(self,label="Cancel",pos = (200,400))
	cancelButton.SetBackgroundColour("green")
        self.Bind(wx.EVT_BUTTON, self.onCancel,cancelButton)

    def onCancel(self,event):
        self.Close(True)

    def OnDeleteSound(self,event):
        global copycmd, src, dest2, nsound, txt
        dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(),defaultFile="", style=wx.OPEN)
        if dlg.ShowModal () == wx.ID_OK:
            picture=dlg.GetPath()
            nsound = dlg.GetFilename ()                                              
        dlg.Destroy()       
        copycmd =  "del " + picture  # delete the file in the folder
        print (copycmd)               
        os.system(copycmd)
        box=wx.MessageDialog(None,"Sound Has been Deleted","Deleted",wx.OK)
        box.ShowModal()
        box.Destroy()
    def OnDeletePicture(self,event):
        global copycmd, src, dest2, nsound, txt
        dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(),defaultFile="", style=wx.OPEN)
        if dlg.ShowModal () == wx.ID_OK:
            picture=dlg.GetPath()
            nsound = dlg.GetFilename ()                                              
        dlg.Destroy()       
        copycmd =  "del " + picture  # delete the file in the folder
        print (copycmd)               
        os.system(copycmd)
        box=wx.MessageDialog(None,"Picture Has been Deleted","Deleted",wx.OK)
        box.ShowModal()
        box.Destroy()
    def OnDelete(self,event):
        def search_file(filename, search_path): # Function for searching the file
            file_found = 0
            paths = string.split(search_path, pathsep)
            for path in paths:
                if exists(join(path, filename)):
                    file_found = 1
                    break
            if file_found:
                return os.path.abspath(join(path, filename))
            else:
                return None
	
        name = self.textCtrl.GetValue()
        image=name+".jpg"
        sound=name+".mp3"
        imagepath=search_file(image,"animals\\")
        print (imagepath)
        soundpath=search_file(sound,"sound\\")
        print (soundpath)
        copycmd = "del "+ imagepath
        copycmd1 = "del "+ soundpath  # delete the file in the folder
        print (copycmd)
        os.system(copycmd)
        print (copycmd1)
        os.system(copycmd1)
        box=wx.MessageDialog(None,"Has been Deleted","Completed",wx.OK)
        box.ShowModal()
        box.Destroy()
        self.Close(True)

class simple(wx.Frame):
    def button1(self): # First show the next button for 5 seconds
        self.slideshow.SetBackgroundColour("green")
        self.insert.SetBackgroundColour("yellow")
        self.delete.SetBackgroundColour("yellow")
        self.exit.SetBackgroundColour("yellow")
        self.slideshow.Show()
        self.insert.Show()
        self.delete.Show()
        self.exit.Show()
        ##############################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by clicking on to the screen
        #########################################################################################
        self.panel.Bind(wx.EVT_LEFT_UP, self.slideshowing)
        self.panel.Bind(wx.EVT_LEFT_UP,self.slideshowing)
        wx.CallLater(5000,self.button2) #5000 - 5 seconds
    def button2(self): # Alternate insert button for the next five seconds
        self.slideshow.SetBackgroundColour("yellow")
        self.delete.SetBackgroundColour("yellow")
        self.exit.SetBackgroundColour("yellow")
        self.insert.SetBackgroundColour("pink")
        self.slideshow.Show()
        self.insert.Show()
        self.delete.Show()
        self.exit.Show()
        ##############################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by clicking on to the screen
        #########################################################################################
        self.panel.Bind(wx.EVT_LEFT_UP, self.inserting)
        self.panel.Bind(wx.EVT_LEFT_UP,self.inserting)
        wx.CallLater(5000,self.button3)

    def button3(self): # Alternate delete button for the next five seconds
        self.slideshow.SetBackgroundColour("yellow")
        self.insert.SetBackgroundColour("yellow")
        self.delete.SetBackgroundColour("red")
        self.exit.SetBackgroundColour("yellow")
        self.slideshow.Show()
        self.insert.Show()
        self.delete.Show()
        self.exit.Show()
        ##############################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by .panelclicking on to the screen
        #########################################################################################
        self.panel.Bind(wx.EVT_LEFT_UP, self.deleting)
        self.panel.Bind(wx.EVT_LEFT_UP,self.deleting)
        wx.CallLater(5000,self.button4)
    def button4(self): # Alternate exit button for the next five seconds
        self.slideshow.SetBackgroundColour("yellow")
        self.insert.SetBackgroundColour("yellow")
        self.delete.SetBackgroundColour("yellow")
        self.exit.SetBackgroundColour("blue")
        self.slideshow.Show()
        self.insert.Show()
        self.delete.Show()
        self.exit.Show()
        ##############################################################################################
        #The following two lines are very important for Vidyasagar. Left mouse click is activated 
        #by clicking on to the screen
        #########################################################################################
        self.panel.Bind(wx.EVT_LEFT_UP, self.exiting)
        self.panel.Bind(wx.EVT_LEFT_UP,self.exiting)
        wx.CallLater(5000,self.button1)

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'cards',size=(1300,750))
        self.panel=wx.Panel(self)
        self.panel.SetBackgroundColour(wx.BLACK)
	font = wx.Font(32, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTSTYLE_NORMAL)
        self.slideshow=wx.Button(self.panel,label='Slideshow',pos=(400,100),size=(400,100))
        self.slideshow.SetBackgroundColour("yellow")
	self.slideshow.SetFont(font)
        self.insert=wx.Button(self.panel,label='Insert',pos=(100,300),size=(400,100))
        self.insert.SetBackgroundColour("yellow")
	self.insert.SetFont(font)
        self.delete=wx.Button(self.panel,label='Delete',pos=(650,300),size=(400,100))
        self.delete.SetBackgroundColour("yellow")
	self.delete.SetFont(font)
        self.exit=wx.Button(self.panel,label='Exit',pos=(400,500),size=(400,100))
        self.exit.SetBackgroundColour("yellow")
	self.exit.SetFont(font)
        #create func
        self.Bind(wx.EVT_BUTTON,self.slideshowing,self.slideshow)
        self.Bind(wx.EVT_BUTTON,self.inserting,self.insert)
        self.Bind(wx.EVT_BUTTON,self.exiting,self.exit)
        self.Bind(wx.EVT_BUTTON,self.deleting,self.delete)
        self.button1()
	
    def slideshowing(self,event):
        MySplash = MySplashScreen()
        MySplash.Show()
        return True
    
    def search_file(filename, search_path): # Function for searching the file
        """Given a search path, find file"""
        file_found = 0
        paths = string.split(search_path, pathsep)
        for path in paths:
            if exists(join(path, filename)):
                file_found = 1
        if file_found:
            return os.path.abspath(join(path, filename))
        else:
            return None
    def inserting(self,event):
        frame = MyFrame()
        frame.Show(True)

    def deleting(self,event):
        frame = MyFrame1()
        frame.Show(True)

    def exiting(self,event):
        self.Close(True)

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=simple(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
