Mna - Version 1.2.0
Copyright (C) 2012-2013, Petros Kyladitis


Description
===========
Mna is a currency converter program writed in Python using the wxPython library
for the user interface and urllib2 library with Google Calculator service API 
to retrieve updated data.

The program supports convertion for 87 currencies. A full list is displayed at 
the end of this file. Connection to the internet is required. The availability
and the quality of the data, based on Google's services.

Also, program uses the local storage and create a file, called "mna.cfg" to
remember the last selected currencies and at the next start set selected them
by default. To work this feature sure that you install the program at a folder
in wich you have priviliges to write.

For more info, updates etc. visit <http://www.multipetros.gr/>


What's new
==========
- Selection for the Precision of the result, with 2, 4, 6 & 8 decimal digits.
- Network traffic minimized, by determine when need to retrieve fresh data.
- OSX UI improvements.
- Code reliability improvements.


UI Shortcuts
============
Enter  : Start the convertion. Same with press the "Convert" button.
Ctrl+Q : Quits the program.
F1     : Show the About box.
Ctrl+2 : Set convertion's precision to 2 decimal digits.
Ctrl+4 : Set convertion's precision to 4 decimal digits.
Ctrl+6 : Set convertion's precision to 6 decimal digits.
Ctrl+8 : Set convertion's precision to 8 decimal digits.


Lisence
=======
Mna is free software, distributed under the terms and conditions of the FreeBSD
License. For full licensing info see the "license.txt" file, distributed with 
this program.


Supported currencies
====================
 - Algerian Dinar (DZD)
 - Argentine Peso (ARS)
 - Australian Dollar (AUD)
 - Bahraini Dinar (BHD)
 - Bolivian Boliviano (BOB)
 - Botswanan Pula (BWP)
 - Brazilian Real (BRL)
 - British Pound Sterling (GBP)
 - Brunei Dollar (BND)
 - Bulgarian Lev (BGN)
 - Canadian Dollar (CAD)
 - Cayman Islands Dollar (KYD)
 - Chilean Peso (CLP)
 - Chinese Yuan (CNY)
 - Colombian Peso (COP)
 - Costa Rican Coln (CRC)
 - Croatian Kuna (HRK)
 - Czech Republic Koruna (CZK)
 - Danish Krone (DKK)
 - Dominican Peso (DOP)
 - Egyptian Pound (EGP)
 - Estonian Kroon (EEK)
 - Euro (EUR)
 - Fijian Dollar (FJD)
 - FYROM Denar (MKD)
 - Honduran Lempira (HNL)
 - Hong Kong Dollar (HKD)
 - Hungarian Forint (HUF)
 - Indian Rupee (INR)
 - Israeli New Sheqel (ILS)
 - Jamaican Dollar (JMD)
 - Japanese Yen (JPY)
 - Jordanian Dinar (JOD)
 - Kazakhstani Tenge (KZT)
 - Kenyan Shilling (KES)
 - Kuwaiti Dinar (KWD)
 - Latvian Lats (LVL)
 - Lebanese Pound (LBP)
 - Lithuanian Litas (LTL)
 - Malaysian Ringgit (MYR)
 - Mauritian Rupee (MUR)
 - Mexican Peso (MXN)
 - Moldovan Leu (MDL)
 - Moroccan Dirham (MAD)
 - Namibian Dollar (NAD)
 - Nepalese Rupee (NPR)
 - Netherlands Antillean Guilder (ANG)
 - New Taiwan Dollar (TWD)
 - New Zealand Dollar (NZD)
 - Nicaraguan Crdoba (NIO)
 - Nigerian Naira (NGN)
 - Norwegian Krone (NOK)
 - Omani Rial (OMR)
 - Pakistani Rupee (PKR)
 - Papua New Guinean Kina (PGK)
 - Paraguayan Guarani (PYG)
 - Peruvian Nuevo Sol (PEN)
 - Philippine Peso (PHP)
 - Polish Zloty (PLN)
 - Qatari Rial (QAR)
 - Romanian Leu (RON)
 - Russian Ruble (RUB)
 - Salvadoran Coln (SVC)
 - Saudi Riyal (SAR)
 - Serbian Dinar (RSD)
 - Seychellois Rupee (SCR)
 - Sierra Leonean Leone (SLL)
 - Singapore Dollar (SGD)
 - Slovak Koruna (SKK)
 - South African Rand (ZAR)
 - South Korean Won (KRW)
 - Sri Lankan Rupee (LKR)
 - Swedish Krona (SEK)
 - Swiss Franc (CHF)
 - Tanzanian Shilling (TZS)
 - Thai Baht (THB)
 - Trinidad and Tobago Dollar (TTD)
 - Tunisian Dinar (TND)
 - Turkish Lira (TRY)
 - UAE Dirham (AED)
 - Ugandan Shilling (UGX)
 - Ukrainian Hryvnia (UAH)
 - Uruguayan Peso (UYU)
 - US Dollar (USD)
 - Uzbekistan Som (UZS)
 - Venezuelan Bolvar (VEF)
 - Yemeni Rial (YER)
