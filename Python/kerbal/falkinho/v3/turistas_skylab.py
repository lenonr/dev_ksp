#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../../')
from base import suborbital

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 150000					# target 		-	VERIFICAR
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	
	# taxa					= 0.16						# progress
	# taxa					= 0.19						# turistas	/ rebocador
	taxa					= 0.10						# turistas	/ laboratorio - salyut
	taxa					= 0.15						# turistas	/ laboratorio - skylab

	# orientation				= 41.7						# TOP-NORMAL
	orientation				= 135						# DOWN-NORMAL	- TRANSFER WINDOW

	suborbital(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()