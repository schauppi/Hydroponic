control_value = -0.8

if control_value > 0.5:
	print("ph value too low")
	
	if control_value >= 0.5 and control_value <= 0.6:
		print("1")
	elif control_value >= 0.6 and control_value <= 0.9:
		print("2")
	elif control_value >= 1:
		print("3")
if control_value < -0.5:
	print("ph value too high")
	if control_value <= -0.5 and control_value >= -0.6:
		print("-1")
	elif control_value <= -0.6 and control_value >= -0.9:
		print("-2")
	elif control_value <= -1:
		print("-3")
