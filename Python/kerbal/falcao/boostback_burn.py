#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	##################################################################################
	#	X				Value			Profile						Weight orbiter	 #
	##################################################################################
	#	
	value			=	-10			# Falcao Science					?? kg 		 #
	#
	#### LEGACY ######################################################################
	#
	# value			=	-10			# Flight Test Cargo				27000 kg 		 #
	#
	##################################################################################

	boostback(value)

main()