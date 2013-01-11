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
from sys import platform

class MainFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        # All GCalc API supported currencies
        currencies=["Algerian Dinar (DZD)", "Argentine Peso (ARS)", "Australian Dollar (AUD)", "Bahraini Dinar (BHD)", "Bolivian Boliviano (BOB)", "Botswanan Pula (BWP)", "Brazilian Real (BRL)", "British Pound Sterling (GBP)", "Brunei Dollar (BND)", "Bulgarian Lev (BGN)", "Canadian Dollar (CAD)", "Cayman Islands Dollar (KYD)", "Chilean Peso (CLP)", "Chinese Yuan (CNY)", "Colombian Peso (COP)", "Costa Rican Coln (CRC)", "Croatian Kuna (HRK)", "Czech Republic Koruna (CZK)", "Danish Krone (DKK)", "Dominican Peso (DOP)", "Egyptian Pound (EGP)", "Estonian Kroon (EEK)", "Euro (EUR)", "Fijian Dollar (FJD)", "FYROM Denar (MKD)", "Honduran Lempira (HNL)", "Hong Kong Dollar (HKD)", "Hungarian Forint (HUF)", "Indian Rupee (INR)", "Israeli New Sheqel (ILS)", "Jamaican Dollar (JMD)", "Japanese Yen (JPY)", "Jordanian Dinar (JOD)", "Kazakhstani Tenge (KZT)", "Kenyan Shilling (KES)", "Kuwaiti Dinar (KWD)", "Latvian Lats (LVL)", "Lebanese Pound (LBP)", "Lithuanian Litas (LTL)", "Malaysian Ringgit (MYR)", "Mauritian Rupee (MUR)", "Mexican Peso (MXN)", "Moldovan Leu (MDL)", "Moroccan Dirham (MAD)", "Namibian Dollar (NAD)", "Nepalese Rupee (NPR)", "Netherlands Antillean Guilder (ANG)", "New Taiwan Dollar (TWD)", "New Zealand Dollar (NZD)", "Nicaraguan Crdoba (NIO)", "Nigerian Naira (NGN)", "Norwegian Krone (NOK)", "Omani Rial (OMR)", "Pakistani Rupee (PKR)", "Papua New Guinean Kina (PGK)", "Paraguayan Guarani (PYG)", "Peruvian Nuevo Sol (PEN)", "Philippine Peso (PHP)", "Polish Zloty (PLN)", "Qatari Rial (QAR)", "Romanian Leu (RON)", "Russian Ruble (RUB)", "Salvadoran Coln (SVC)", "Saudi Riyal (SAR)", "Serbian Dinar (RSD)", "Seychellois Rupee (SCR)", "Sierra Leonean Leone (SLL)", "Singapore Dollar (SGD)", "Slovak Koruna (SKK)", "South African Rand (ZAR)", "South Korean Won (KRW)", "Sri Lankan Rupee (LKR)", "Swedish Krona (SEK)", "Swiss Franc (CHF)", "Tanzanian Shilling (TZS)", "Thai Baht (THB)", "Trinidad and Tobago Dollar (TTD)", "Tunisian Dinar (TND)", "Turkish Lira (TRY)", "UAE Dirham (AED)", "Ugandan Shilling (UGX)", "Ukrainian Hryvnia (UAH)", "Uruguayan Peso (UYU)", "US Dollar (USD)", "Uzbekistan Som (UZS)", "Venezuelan Bolvar (VEF)", "Yemeni Rial (YER)"]

        # Ini name, section, parameters
        self.INI_FILE = "mna.cfg"
        self.INI_SECTION = "main"
        self.INI_PARAM_FROM = "from"
        self.INI_PARAM_TO = "to"
        self.INI_PARAM_PRECISION = "precision"

        # Initialize variables that determinate the need of retrieve fresh data from the network
        self.current_currency = 0   # the current curenncies exchange rate
        self.last_from = ""         # the last selected 'from' currency
        self.last_to = ""           # the last selected 'to' currency

        kwds["style"] = wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.RESIZE_BORDER
        wx.Frame.__init__(self, *args, **kwds)

        # Main frame controls
        self.label_from = wx.StaticText(self, -1, "From")
        self.combo_box_from = wx.ComboBox(self, -1, choices=currencies, style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.combo_box_from.SetToolTip(wx.ToolTip("Select the currency you want to convert from"))
        self.text_ctrl_from = wx.TextCtrl(self, -1, "")
        self.text_ctrl_from.SetToolTip(wx.ToolTip("Ammount you want to convert"))
        self.label_to = wx.StaticText(self, -1, "To")
        self.combo_box_to = wx.ComboBox(self, -1, choices=currencies, style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.combo_box_to.SetToolTip(wx.ToolTip("Select the currency you want to convert to"))
        self.text_ctrl_to = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.text_ctrl_to.SetToolTip(wx.ToolTip("Converted ammount"))
        self.button_convert = wx.Button(self, -1, "Convert")
        self.button_convert.SetToolTip(wx.ToolTip("Click to convert the ammount to selected currency"))
        self.button_convert.SetDefault()

        # Menu Bar
        self.frame_main_menubar = wx.MenuBar()
        # If NOT run on OSX create a File menu and append an Exit menu item. At OSX is unnecessary because of App Menu
        if platform != "darwin":
            self.menu_file = wx.Menu()
            self.menu_item_exit = wx.MenuItem(self.menu_file, wx.ID_EXIT, "&Exit\tCtrl+Q", "Quit the program", wx.ITEM_NORMAL)
            self.menu_file.AppendItem(self.menu_item_exit)
            self.frame_main_menubar.Append(self.menu_file, "&File")
        self.menu_precision = wx.Menu()
        self.menu_item_two_decs = wx.MenuItem(self.menu_precision, 202, "&2 decimals\tCtrl+2", "Precision with 2 decimal digits", wx.ITEM_RADIO)
        self.menu_precision.AppendItem(self.menu_item_two_decs)
        self.menu_item_four_decs = wx.MenuItem(self.menu_precision, 204, "&4 decimals\tCtrl+4", "Precision with 4 decimal digits", wx.ITEM_RADIO)
        self.menu_precision.AppendItem(self.menu_item_four_decs)
        self.menu_item_six_decs = wx.MenuItem(self.menu_precision, 206, "&6 decimals\tCtrl+6", "Precision with 6 decimal digits", wx.ITEM_RADIO)
        self.menu_precision.AppendItem(self.menu_item_six_decs)
        self.menu_item_eight_decs = wx.MenuItem(self.menu_precision, 208, "&8 decimals\tCtrl+8", "Precision with 8 decimal digits", wx.ITEM_RADIO)
        self.menu_precision.AppendItem(self.menu_item_eight_decs)
        self.frame_main_menubar.Append(self.menu_precision, "&Precision")
        self.menu_help = wx.Menu()
        self.menu_item_about = wx.MenuItem(self.menu_help, wx.ID_ABOUT, "&About\tF1", "Show about info", wx.ITEM_NORMAL)
        self.menu_help.AppendItem(self.menu_item_about)
        self.frame_main_menubar.Append(self.menu_help, "&Help")
        self.SetMenuBar(self.frame_main_menubar)

        # Add status bar
        self.statusbar = self.CreateStatusBar()

        self.__set_properties()
        self.__do_layout()

        # Add event handlers
        self.Bind(wx.EVT_BUTTON, self.OnConvert, self.button_convert)
        self.Bind(wx.EVT_COMBOBOX, self.OnConvert, self.combo_box_from)
        self.Bind(wx.EVT_COMBOBOX, self.OnConvert, self.combo_box_to)
        # If NOT run on OSX bind handler for Exit menu item
        if platform != "darwin":
            self.Bind(wx.EVT_MENU, self.OnExit, self.menu_item_exit)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.menu_item_about)
        self.Bind(wx.EVT_MENU, self.OnPrecisionChange, self.menu_item_two_decs)
        self.Bind(wx.EVT_MENU, self.OnPrecisionChange, self.menu_item_four_decs)
        self.Bind(wx.EVT_MENU, self.OnPrecisionChange, self.menu_item_six_decs)
        self.Bind(wx.EVT_MENU, self.OnPrecisionChange, self.menu_item_eight_decs)
        # Bind event handler for double click on status bar
        self.statusbar.Bind(wx.EVT_LEFT_DCLICK, self.OnDblClickStatus, self.statusbar)


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
            self.current_precision = int(config.get(self.INI_SECTION, self.INI_PARAM_PRECISION))
            self.combo_box_from.SetSelection(long(config.get(self.INI_SECTION, self.INI_PARAM_FROM)))
            self.combo_box_to.SetSelection(long(config.get(self.INI_SECTION, self.INI_PARAM_TO)))
        except:
            self.current_precision = 2
            self.combo_box_from.SetSelection(83)
            self.combo_box_to.SetSelection(22)        

        # Start-up values, used to determinate selection changes at the program's exit
        self.init_from = self.combo_box_from.GetCurrentSelection()
        self.init_to = self.combo_box_to.GetCurrentSelection()
        self.init_precision = self.current_precision
        self.SetInitPrecision(self.init_precision)


    def __do_layout(self):
        # Use a vertical box sizer to fit menu bar, grid sizer with controls & status bar
        box_sizer = wx.BoxSizer(wx.VERTICAL)

        # Place controls to a flex grid sizer, with empty cells arround them
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

        # Add grid sizer with controls to box sizer and set the box sizer
        # as the sizer for the main frame
        box_sizer.Add(grid_sizer_main, 1, wx.EXPAND, 0)
        self.SetSizerAndFit(box_sizer)
        box_sizer.Fit(self)
        self.Layout()


    def SetInitPrecision(self, precision):
        # Set checked the appropriate menu item, based on precision param
        if precision == 4:
            self.menu_item_four_decs.Check(True)
        elif precision == 6:
            self.menu_item_six_decs.Check(True)
        elif precision == 8:
            self.menu_item_eight_decs.Check(True)
        else:
            self.menu_item_two_decs.Check(True)


    def OnDblClickStatus(self, event):
        # If status bar have text, display it on a text box
        if self.statusbar.StatusText != "":
            wx.MessageBox(self.statusbar.StatusText, "Status info",wx.OK | wx.ICON_INFORMATION)



    def OnExit(self, event):
        # 1st of all hide the main form
        self.Hide()

        # If selected currencies differs from the initial selected
        # try to save to the ini configuration file, on error just exit
        try:
            if (long(self.init_from) != self.combo_box_from.GetCurrentSelection()) or (long(self.init_to) != self.combo_box_to.GetCurrentSelection() or self.init_precision != self.current_precision):
                cfgfile = open(self.INI_FILE,"w")
                config = ConfigParser.ConfigParser()
                config.read(self.INI_FILE)

                # Try to add the main section, if exist an exception will be thrown, in that case resume next
                try:
                    config.add_section(self.INI_SECTION)
                except:
                    pass

                # Set the values to ini parameters and save
                config.set(self.INI_SECTION, self.INI_PARAM_PRECISION, str(self.current_precision))
                config.set(self.INI_SECTION, self.INI_PARAM_FROM, str(self.combo_box_from.GetCurrentSelection()))
                config.set(self.INI_SECTION, self.INI_PARAM_TO, str(self.combo_box_to.GetCurrentSelection()))
                config.write(cfgfile)
                cfgfile.close()
        except:
            pass

        self.Destroy()


    def OnAbout(self, event):
        # create and show an about dialog box
        info = wx.AboutDialogInfo()
        info.SetName("Mna Currency Converter")
        info.SetVersion("1.2.0")
        info.SetCopyright("Copyright (C) 2012, Petros Kyladitis")
        info.Description = wordwrap("A currency converter program for Python, using wxPython for the GUI and urllib2 library with Google Calculator service API to retrieve updated data.", 350, wx.ClientDC(self))
        info.SetWebSite("http://www.multipetros.gr")
        info.License = wordwrap("This program is free software, distributed under the terms and conditions of the FreeBSD License. For full licensing info see the \"license.txt\" file, distributed with this program", 350, wx.ClientDC(self))
        info.SetIcon(self.ico) # Declared at self.__set_properties()
        wx.AboutBox(info)


    def OnPrecisionChange(self, event): 
        # Get the id of the menu item that raise the event. The ids are especially setted
        # as (item meaning + 200), so it's easy to find the selected precision value
        self.current_precision = event.GetId() - 200
        self.DoConvertion(False)


    def OnConvert(self, event):
        # If the current selected currencies is the same as the last convertion,
        # start the convertion without retrieve fresh data, else convert with  retriving new data 
        # and save the selected curencies values as the last selected.
        if (self.combo_box_from.Value == self.last_from) and (self.combo_box_to.Value == self.last_to):
            self.DoConvertion(False)
        else:
            self.DoConvertion()
            self.last_from = self.combo_box_from.Value
            self.last_to = self.combo_box_to.Value


    def DoConvertion(self, retrieveFreshData=True):

        # Try to convert the user inputed amount into a float, on error set it to 1.0
        try:
            user_input_ammount = float(self.text_ctrl_from.Value)
        except:
            user_input_ammount = 1.0
            self.text_ctrl_from.Value = str(user_input_ammount)

        # Convert if negative ammount to absolute value
        if user_input_ammount < 0:
            user_input_ammount = -1 * user_input_ammount
            self.text_ctrl_from.Value = str(user_input_ammount)

        if (retrieveFreshData == True) or (self.current_currency == 0):
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
                self.SetStatusText("Retrieving data. Please wait...")
                gcalc_currency = urlopen("http://www.google.com/ig/calculator?hl=en&q=" + from_cur_name + "%3D%3F" + to_cur_name).read()
                gcalc_currency_start = gcalc_currency.find("rhs: \"") + 6
                gcalc_currency_end = gcalc_currency.find(" ", gcalc_currency_start)
                self.current_currency = float(gcalc_currency[gcalc_currency_start:gcalc_currency_end])
                self.SetStatusText("Exchange rate: 1 " + from_cur_name + " = " + str(self.current_currency) + " " + to_cur_name)
            except Exception as details:
                self.SetStatusText("Can\'t retrieve data from Google Calc Service. " + str(details))
                self.current_currency = 0 # To force retrieve data at the next DoConvertion(False) call
                return

        result =  user_input_ammount * self.current_currency
        self.text_ctrl_to.Value = str(round(result,self.current_precision))

# end of class MainFrame


class MnaApp(wx.App):
    # Override method for handling kAEReopenApplication to work correctly with the Dock at OSX
    def MacReopenApp(self):
        try:
            self.GetTopWindow().Raise()
        except:
            pass


if __name__ == "__main__":
    app = MnaApp(False)
    frame_main = MainFrame(None, -1, "")
    app.SetTopWindow(frame_main)
    frame_main.Show()
    app.MainLoop()
