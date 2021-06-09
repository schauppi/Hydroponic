import lcddriver_display_1
from time import *
 
lcd = lcddriver_display_1.lcd()
lcd.lcd_clear()


def display_1(ec, ph):
	
	string_ec_1 = "EC: "
	ec_string = str(ec)
	string_ec = string_ec_1 + ec_string
	string_ph_1 = "PH: "
	ph_string = str(ph)
	string_ph = string_ph_1 + ph_string

	lcd.lcd_display_string(string_ph, 1)
	lcd.lcd_display_string(string_ec,  2)
