import wx,pyglet

import wx.lib.newevent
SomeNewEvent, EVT_LOAD_SOUND = wx.lib.newevent.NewEvent()
class TestFrame(wx.Frame):
    def __init__(self,parent,id,title):
        self.frame = wx.Frame.__init__(self,parent,id,title,pos=(10,10),size = (800,600))
        #wx.Frame.__init__(self,parent,id,title,pos = (10,10), size = (800,600), title = "test")
        p = wx.Panel (self)
        name = 'animals/monkey.jpg'
        fgs = wx.BoxSizer(wx.VERTICAL)        
        img = wx.Image(name,wx.BITMAP_TYPE_ANY)
        sb = wx.StaticBitmap(p,-1,wx.BitmapFromImage(img))
        fgs.Add(sb)
        p.SetSizerAndFit(fgs)        
        self.Center()
        self.Fit()
        self.Show(True)
        wx.FutureCall(1000, self.OnSound)
        
        
    def OnSound(self):
        music = pyglet.media.load('sound/monkey.mp3',streaming=False)        
        def exiter(dt):
                    pyglet.app.exit()
        music.play()
        pyglet.clock.schedule_once(exiter,3)
        pyglet.app.run() 
        self.Refresh ()
         
        
app = wx.PySimpleApp()
frm = TestFrame(None,-1,"Test")
app.MainLoop()
 
