import wx,pyglet
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
        
        music = wx.Sound('sound/one.wav')        
        if music.IsOk():
            music.Play(wx.SOUND_ASYNC)
        else:
            wx.MessageBox("Invalid sound file","Error")
         
        
app = wx.PySimpleApp()
frm = TestFrame(None,-1,"Test")
frm.Show()
app.MainLoop()
