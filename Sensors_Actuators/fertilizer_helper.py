# coding=utf8

#Fert A - Pump 3 - 39sek/3cl
#Fert B - Pump 4 - 41sek/3cl

#Verdünnung - 1:333
#25 / 333 = 0,075l
#0,075l = 75ml
#75ml = 7,5cl
# 1 cl = 10ml (*10)

dilution = 333.0
dosing_pump_3_30_ml = 39
dosing_pump_4_30_ml = 41

def fertilize(water_level):
	
	#calculate fert amount
	amount_fert = (round(water_level / dilution, 3)) * 100
	#calculate tpump time
	time_dosing_pump_3 = (amount_fert / 3) * dosing_pump_3_30_ml
	time_dosing_pump_4 = (amount_fert / 3) * dosing_pump_4_30_ml
	
	return time_dosing_pump_3, time_dosing_pump_4

