# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version 3.9.0 Jun  2 2020)
# http://www.wxformbuilder.org/
##
# PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from finder import get_results

###########################################################################
# Class MainFrame
###########################################################################


class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(
            300, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.label_address = wx.StaticText(
            self, wx.ID_ANY, u"Адрес", wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_address.Wrap(-1)

        main_sizer.Add(self.label_address, 0, wx.ALL, 5)

        self.text_address = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"address")
        main_sizer.Add(self.text_address, 0, wx.ALL | wx.EXPAND, 5)

        self.button_search = wx.Button(
            self, wx.ID_ANY, u"Поиск", wx.DefaultPosition, wx.DefaultSize, 0)
        main_sizer.Add(self.button_search, 0, wx.ALL | wx.EXPAND, 5)

        self.label_error = wx.StaticText(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.label_error.Wrap(-1)

        main_sizer.Add(self.label_error, 0, wx.ALL, 5)

        self.gs = wx.GridSizer(0, 2, 0, 0)

        main_sizer.Add(self.gs, 1, wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_search.Bind(wx.EVT_BUTTON, self.search)

    def __del__(self):
        self.clear_table()

    def clear_table(self):
        for item in self.gs.GetChildren():
            item.GetWindow().Destroy()

    # Virtual event handlers, overide them in your derived class
    def search(self, event):
        self.clear_table()
        address = self.text_address.GetValue()
        data = get_results(address)
        if isinstance(data, str):
            self.label_error.SetLabel(data)
        elif isinstance(data, dict):
            self.label_error.SetLabel("")
            for key in data:
                self.gs.Add(wx.StaticText(self, label=key))
                self.gs.Add(wx.StaticText(self, label=data[key]))
        event.Skip()

