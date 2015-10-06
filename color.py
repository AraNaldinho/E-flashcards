
import wx 
 
class ButtonFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, -1, 'Button Example',  
                size=(300, 100)) 
        panel = wx.Panel(self, -1) 
        self.button = wx.Button(panel, -1, "Hello", pos=(50, 20)) 
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnClick, self.button) 
        self.button.SetDefault() 
 
    def OnClick(self, event): 
        self.button.SetLabel("Clicked") 
        self.button.SetBackgroundColour('blue') 
if __name__ == '__main__': 
    app = wx.PySimpleApp() 
    frame = ButtonFrame() 
    frame.Show() 
    app.MainLoop() 
