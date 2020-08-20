#!/usr/bin/env python
import pmultiwii

def msp_callback(msp_cmd,dataSize):
    #print "received cmd " + str(msp_cmd) + ", " + str(dataSize)
    if msp_cmd == 10:
        print msp.msp_name['name']
    #if msp_cmd == 84:
    #    print msp.msp_osd_config['osd_items'][8] # craft name
    #if msp_cmd == 110:
    #    print msp.msp_altitude['vspeed']
    #if msp_cmd == 84:
    #    print msp.msp_osd_config['osd_items'][14][0] # nsats
    #    print msp.msp_osd_config['osd_items'][30][0] # home dir
    #if msp_cmd == 107:
    #    print msp.msp_comp_gps['GPS_directionToHome']
    #if msp_cmd == 106:
    #    print msp.msp_raw_gps['GPS_speed']            # ground speed
    #    print msp.msp_osd_config['osd_items'][8]
    #if msp_cmd == 130:
    #    print msp.msp_battery_state['current']
    #if msp_cmd == 108:
    #    print msp.msp_attitude['yaw'] #
    #if msp_cmd == 84:
    #    print msp.msp_osd_config['osd_items'][26] # pitch/airspeed override

msp = pmultiwii.Multiwii(None, "localhost", 5763, True, msp_callback)
try:
    print "Connecting..."
    msp.receiveTcpData()
except Exception,error:
    print "Error on Main"+ str(error)
