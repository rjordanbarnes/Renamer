import wx
import ui

TITLE = "Renaming Tool"
WIDTH = 900
HEIGHT = 600


def main():
    app = wx.App(False)
    frame = ui.MainFrame(None, TITLE, WIDTH, HEIGHT)
    frame.Show()
    app.MainLoop()

main()
