# -*- coding: utf-8 -*-
#!/usr/bin/env python

value=18948       	# kg
fuel=15840			# CHECK!!

def calc(value):	
	mass=16948      # 14.948 kg, final stage
	taxa=0.145      # 0.145% fuel, first stage

	plus_less=0.66
	mass_plus=mass+(mass*plus_less)
	mass_less=mass-(mass*plus_less)

	heavy = False
	light = False

	x = (value * taxa / mass)

	# print 'Valor de x antes:',x
	# print mass_plus
	# print mass_less

	if value > mass_plus or value < mass_less:
		print ('Very heavy or very light')			
	else:
		if value > mass:
			if x >= 0.01:
				x = x*0.10

			x = taxa - x
		elif value < mass:
			x = taxa + x 
		else:
			x = taxa

	# print 'Valor de x depois:',x
	print "Full fuel launch:", fuel
	print
	print "First stage[PERCENT]:" , x
	print "Firt stage rescue:", (fuel)-(fuel-(x*value))

calc(value)
