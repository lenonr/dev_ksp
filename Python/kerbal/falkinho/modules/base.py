#!/usr/bin/env python

# Reference: https://krpc.github.io/krpc/tutorials/launch-into-orbit.html

import math
import time
import krpc

conn = krpc.connect(name='Launch into orbit')
vessel = conn.space_center.active_vessel
ksc = conn.space_center
nave = ksc.active_vessel
rf = nave.orbit.body.reference_frame

# Set up streams for telemetry
# general
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')    

# landing
recursos_estagio_1 = nave.resources_in_decouple_stage(stage=2, cumulative=False)
combustivel1 = conn.add_stream(recursos_estagio_1.amount, 'LiquidFuel')
recursos_estagio_2 = nave.resources_in_decouple_stage(stage=0, cumulative=False)
combustivel2 = conn.add_stream(recursos_estagio_2.amount, 'LiquidFuel')

def launch(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time):        
    print('Systems nominal for launch. T-3 seconds!')
    time.sleep(3)

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    
    print('Ignition!')

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0
    while True:      
        if altitude() == turn_start_altitude:
            print('----Pitch/Row')

        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, 90)

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                print('----Strongback separated')
                print('LIFTOOF!')                        

        # MAX-Q
        if altitude() == maxq_begin:
            print('----Max-Q')

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50
        else:
            vessel.control.throttle = 1.0

        if vessel.available_thrust == 0.0:                
            vessel.control.throttle = 0.30

            vessel.control.activate_next_stage()        
            print('MECO-1')        
            time.sleep(1)

            print('----Separation first stage')            

            vessel.control.activate_next_stage()        
            print('MES-1')      
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print('----Approaching target apoapsis')
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print('MECO-2')
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print('----Coasting out of atmosphere')
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print('----Planning circularization burn')
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print('----Orientating ship for circularization burn')
    vessel.control.rcs = True
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print('----Waiting until circularization burn')
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print('----Ready to execute burn')
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print('MES-2')   
    vessel.control.throttle = 1.0         
        
    time.sleep(burn_time - 0.1)
    print('----Fine tuning')
    vessel.control.throttle = 0.30
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    while True:
        if vessel.available_thrust == 0.0:                
            vessel.control.throttle = 0.10

            vessel.control.activate_next_stage()        
            print('MECO-3')        
            time.sleep(3)

            print('----Separation second stage')            

            vessel.control.activate_next_stage()        
            print('MES-3')        
            break

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()

    # Resources
    vessel.control.sas = True
    vessel.control.rcs = False

    for antenna in nave.parts.antennas:
        if antenna.deployable:
            antenna.deployed = True
            sleep(1)
        for painelsolar in nave.parts.solar_panels:
            if painelsolar.deployable:
                painelsolar.deployed = True
                sleep(1)

    print('Launch complete')

def landing():    
    print('Start burn for reentry... T-5 seconds')