#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falcao_landing_zone

def main():	
	#################################################################################
	#
	target_altitude         = 150000
	turn_end_altitude       = (target_altitude/1.5)		
	#
	##########################################################################################
	#		X					Value				Profile					Weight orbiter	 #
	##########################################################################################
	#	
	taxa					= 	0.20				# Falcao Science			???? kg	 	#
	#
	#### LEGACY ##############################################################################
	#
	# taxa					= 	0.20				# Flight Test Cargo			27000 kg	 #
	#
	##########################################################################################

	falcao_landing_zone(1000,turn_end_altitude,target_altitude, 20000, 36000, taxa, 90, True)

main()