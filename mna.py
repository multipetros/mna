#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Mna - A Currency Converter program
# Copyright (c) 2012, Petros Kyladitis <http://www.multipetros.gr/>
# This is free software, distributed under the FreeBSD Lisence

import wx
from wx.lib.wordwrap import wordwrap
from urllib2 import urlopen
import ConfigParser

class MainFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        #all GCalc API supported currencies
        currencies=[ "Algerian Dinar (DZD)",  "Argentine Peso (ARS)",  "Australian Dollar (AUD)",  "Bahraini Dinar (BHD)",  "Bolivian Boliviano (BOB)",  "Botswanan Pula (BWP)",  "Brazilian Real (BRL)",  "British Pound Sterling (GBP)",  "Brunei Dollar (BND)",  "Bulgarian Lev (BGN)",  "Canadian Dollar (CAD)",  "Cayman Islands Dollar (KYD)",  "Chilean Peso (CLP)",  "Chinese Yuan (CNY)",  "Colombian Peso (COP)",  "Costa Rican Coln (CRC)",  "Croatian Kuna (HRK)",  "Czech Republic Koruna (CZK)",  "Danish Krone (DKK)",  "Dominican Peso (DOP)",  "Egyptian Pound (EGP)",  "Estonian Kroon (EEK)",  "Euro (EUR)",  "Fijian Dollar (FJD)",  "FYROM Denar (MKD)",  "Honduran Lempira (HNL)",  "Hong Kong Dollar (HKD)",  "Hungarian Forint (HUF)",  "Indian Rupee (INR)",  "Israeli New Sheqel (ILS)",  "Jamaican Dollar (JMD)",  "Japanese Yen (JPY)",  "Jordanian Dinar (JOD)",  "Kazakhstani Tenge (KZT)",  "Kenyan Shilling (KES)",  "Kuwaiti Dinar (KWD)",  "Latvian Lats (LVL)",  "Lebanese Pound (LBP)",  "Lithuanian Litas (LTL)",  "Malaysian Ringgit (MYR)",  "Mauritian Rupee (MUR)",  "Mexican Peso (MXN)",  "Moldovan Leu (MDL)",  "Moroccan Dirham (MAD)",  "Namibian Dollar (NAD)",  "Nepalese Rupee (NPR)",  "Netherlands Antillean Guilder (ANG)",  "New Taiwan Dollar (TWD)",  "New Zealand Dollar (NZD)",  "Nicaraguan Crdoba (NIO)",  "Nigerian Naira (NGN)",  "Norwegian Krone (NOK)",  "Omani Rial (OMR)",  "Pakistani Rupee (PKR)",  "Papua New Guinean Kina (PGK)",  "Paraguayan Guarani (PYG)",  "Peruvian Nuevo Sol (PEN)",  "Philippine Peso (PHP)",  "Polish Zloty (PLN)",  "Qatari Rial (QAR)",  "Romanian Leu (RON)",  "Russian Ruble (RUB)",  "Salvadoran Coln (SVC)",  "Saudi Riyal (SAR)",  "Serbian Dinar (RSD)",  "Seychellois Rupee (SCR)",  "Sierra Leonean Leone (SLL)",  "Singapore Dollar (SGD)",  "Slovak Koruna (SKK)",  "South African Rand (ZAR)",  "South Korean Won (KRW)",  "Sri Lankan Rupee (LKR)",  "Swedish Krona (SEK)",  "Swiss Franc (CHF)",  "Tanzanian Shilling (TZS)",  "Thai Baht (THB)",  "Trinidad and Tobago Dollar (TTD)",  "Tunisian Dinar (TND)",  "Turkish Lira (TRY)", "UAE Dirham (AED)", "Ugandan Shilling (UGX)",  "Ukrainian Hryvnia (UAH)",  "Uruguayan Peso (UYU)",  "US Dollar (USD)",  "Uzbekistan Som (UZS)",  "Venezuelan Bolvar (VEF)",  "Yemeni Rial (YER)"]

        #ini name, section, parameters
        self.INI_FILE = "mna.cfg"
        self.INI_SECTION = "main"
        self.INI_PARAM_FROM = "from"
        self.INI_PARAM_TO = "to"

        kwds["style"] = wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.RESIZE_BORDER
        wx.Frame.__init__(self, *args, **kwds)

        # Main frame controls
        self.label_from = wx.StaticText(self, -1, "From")
        self.combo_box_from = wx.ComboBox(self, -1, choices=currencies, style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.combo_box_from.SetToolTip(wx.ToolTip("Select the currency you want to covert from"))
        self.text_ctrl_from = wx.TextCtrl(self, -1, "")
        self.text_ctrl_from.SetToolTip(wx.ToolTip("Ammount you want to covert"))
        self.label_to = wx.StaticText(self, -1, "To")
        self.combo_box_to = wx.ComboBox(self, -1, choices=currencies, style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.combo_box_to.SetToolTip(wx.ToolTip("Select the currency you want to covert to"))
        self.text_ctrl_to = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.text_ctrl_to.SetToolTip(wx.ToolTip("Coverted ammount"))
        self.button_convert = wx.Button(self, -1, "Covert")
        self.button_convert.SetToolTip(wx.ToolTip("Click to convert the ammount to selected currency"))
        self.button_convert.SetDefault()

        # Menu Bar
        self.frame_main_menubar = wx.MenuBar()
        self.menu_file = wx.Menu()
        self.menu_item_exit = wx.MenuItem(self.menu_file, wx.ID_EXIT, "&Exit\tCtrl+Q", "Quit the program", wx.ITEM_NORMAL)
        self.menu_file.AppendItem(self.menu_item_exit)
        self.frame_main_menubar.Append(self.menu_file, "&File")
        self.menu_help = wx.Menu()
        self.menu_item_about = wx.MenuItem(self.menu_help, wx.ID_HELP, "&About\tF1", "Show about info", wx.ITEM_NORMAL)
        self.menu_help.AppendItem(self.menu_item_about)
        self.frame_main_menubar.Append(self.menu_help, "&Help")
        self.SetMenuBar(self.frame_main_menubar)

        # Add status bar
        self.statusbar = self.CreateStatusBar()

        self.__set_properties()
        self.__do_layout()

        # Add event handlers
        self.Bind(wx.EVT_BUTTON, self.onConvertClick, self.button_convert)
        self.Bind(wx.EVT_MENU, self.onExitClick, self.menu_item_exit)
        self.Bind(wx.EVT_MENU, self.onAboutClick, self.menu_item_about)
        self.Bind(wx.EVT_CLOSE, self.onExitClick)


    def __set_properties(self):
        self.SetTitle("Mna Currency Converter")
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        # Application icon
        self.ico = wx.Icon("icon.gif", wx.BITMAP_TYPE_GIF)
        self.SetIcon(self.ico)

        # Load ini parameters and set the selected values at combo boxes
        # If ini or parameters missing, not valid or other error set selected USD and EUR
        try:
            config = ConfigParser.ConfigParser()
            config.read(self.INI_FILE)
            self.combo_box_from.SetSelection(long(config.get(self.INI_SECTION, self.INI_PARAM_FROM)))
            self.combo_box_to.SetSelection(long(config.get(self.INI_SECTION, self.INI_PARAM_TO)))
        except:
            self.combo_box_from.SetSelection(83)
            self.combo_box_to.SetSelection(22)

        # Start-up values, used to determinate selection changes at the program's exit
        self.init_from = self.combo_box_from.GetCurrentSelection()
        self.init_to = self.combo_box_to.GetCurrentSelection()


    def __do_layout(self):
        # place controls to a flex grid sizer, with empty cells arround the
        grid_sizer_main = wx.FlexGridSizer(5, 5, 6, 6)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add(self.label_from, 0, 0, 0)
        grid_sizer_main.Add(self.combo_box_from, 0, 0, 0)
        grid_sizer_main.Add(self.text_ctrl_from, 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add(self.label_to, 0, 0, 0)
        grid_sizer_main.Add(self.combo_box_to, 0, 0, 0)
        grid_sizer_main.Add(self.text_ctrl_to, 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add(self.button_convert, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        grid_sizer_main.Add((5, 5), 0, 0, 0)
        self.SetSizerAndFit(grid_sizer_main)
        grid_sizer_main.Fit(self)
        self.Layout()


    def onExitClick(self, event):
        #1st of all hide the main form
        self.Hide()

        #if selected currencies differs from the initial selected
        #try to save to the ini configuration file, on error just exit
        try:
            if (long(self.init_from) != self.combo_box_from.GetCurrentSelection()) or (long(self.init_to) != self.combo_box_to.GetCurrentSelection()):
                cfgfile = open(self.INI_FILE,"w")
                config = ConfigParser.ConfigParser()
                config.read(self.INI_FILE)

                #try to add the main section, if exist an exception will be thrown, in that case resume next
                try:
                    config.add_section(self.INI_SECTION)
                except:
                    pass

                #set the values to ini parameters and save
                config.set(self.INI_SECTION, self.INI_PARAM_FROM, str(self.combo_box_from.GetCurrentSelection()))
                config.set(self.INI_SECTION, self.INI_PARAM_TO, str(self.combo_box_to.GetCurrentSelection()))
                config.write(cfgfile)
                cfgfile.close()
        except:
            pass

        self.Destroy()


    def onAboutClick(self, event):
        #create and show an about dialog box
        info = wx.AboutDialogInfo()
        info.SetName("Mna Currency Converter")
        info.SetVersion("1.0.1")
        info.SetCopyright("Copyright (C) 2012, Petros Kyladitis")
        info.Description = wordwrap("A currency converter program for Python, using wxPython for the GUI and urllib2 library with Google Calculator service API to retrieve updated data.", 350, wx.ClientDC(self))
        info.SetWebSite("http://www.multipetros.gr")
        info.License = wordwrap("This program is free software, distributed under the terms and conditions of the FreeBSD License. For full licensing info see the \"license.txt\" file, distributed with this program", 350, wx.ClientDC(self))
        info.SetIcon(self.ico) #declared at self.__set_properties()
        wx.AboutBox(info)


    def onConvertClick(self, event):
        # Parse the 3-letter international name of selected currencies, which are
        # inside of the parentheses "name of cur (xxx)" of selected combo box values
        from_cur_name = self.combo_box_from.Value[(self.combo_box_from.Value.find("(")+1):self.combo_box_from.Value.find(")")]
        to_cur_name = self.combo_box_to.Value[(self.combo_box_to.Value.find("(")+1):self.combo_box_to.Value.find(")")]

        # Read the returned string from the Google Calc service, when passing the above cur names
        # the returned string looks like {lhs: "1 U.S. dollar",rhs: "0.758495146 Euros",error: "",icc: true}
        # or {lhs: "",rhs: "",error: "4",icc: false} when an error occured
        # So, try to parse the value after the rhs: " and before the next space wich represend the exchange rate
        # and use it to calculate the result. Or error, show the exception message to the status bar.
        try:
            gcalc_currency = urlopen("http://www.google.com/ig/calculator?hl=en&q=" + from_cur_name + "%3D%3F" + to_cur_name).read()
            gcalc_currency_start = gcalc_currency.find("rhs: \"") + 6
            gcalc_currency_end = gcalc_currency.find(" ", gcalc_currency_start)
            user_input_ammount = float(self.text_ctrl_from.Value)
            try:
                current_currency = float(gcalc_currency[gcalc_currency_start:gcalc_currency_end])
            except:
                raise Exception("This conversion isn\'t currently available from Google Calc")
            result =  user_input_ammount * current_currency
            self.text_ctrl_to.Value = str(round(result,2))
            self.SetStatusText("Exchange rate: 1 " + from_cur_name + " = " + str(current_currency) + " " + to_cur_name)
        except ValueError:
             self.SetStatusText("User input isn\'t valid number")
        except urllib2.URLError:
             self.SetStatusText("Can\'t retrieve data from Google Calc Service")
        except Exception as details:
             self.SetStatusText(str(details))

# end of class MainFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_main = MainFrame(None, -1, "")
    app.SetTopWindow(frame_main)
    frame_main.Show()
    app.MainLoop()
