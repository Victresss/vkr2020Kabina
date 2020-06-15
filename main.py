from frame import MainFrame
import wx

if __name__ == '__main__':
    app = wx.App(False) 
    frame = MainFrame(None) 
    frame.Show(True) 
    app.MainLoop() 
