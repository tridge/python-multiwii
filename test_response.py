#!/usr/bin/env python
import pmultiwii
import threading
import time

msp_commands = [pmultiwii.Multiwii.MSP_NAME, pmultiwii.Multiwii.MSP_ATTITUDE, pmultiwii.Multiwii.MSP_STATUS, pmultiwii.Multiwii.MSP_OSD_CONFIG]
msp_command_idx = 0

def send():
    global msp, msp_commands, msp_command_idx
    while True:
        msp.sendTcpRequestMSP(msp.requestMSP(msp_commands[msp_command_idx]))
        msp_command_idx = (msp_command_idx+1)%3
        time.sleep(0.5)

def receive():
    global msp
    while True:
        msp.processTcpData()

def msp_callback(msp_cmd,dataSize):
    print "received cmd " + str(msp_cmd) + ", " + str(dataSize)
    if msp_cmd == 10:
        print msp.msp_name['name']
    if msp_cmd == 84:
        print msp.msp_osd_config['osd_items'][8] # craft name
    if msp_cmd == 110:
        print msp.msp_altitude['vspeed']
    #if msp_cmd == 84:
    #    print msp.msp_osd_config['osd_items'][14][0] # nsats
    #    print msp.msp_osd_config['osd_items'][30][0] # home dir
    if msp_cmd == 107:
        print msp.msp_comp_gps['GPS_directionToHome']
    if msp_cmd == 106:
        print msp.msp_raw_gps['GPS_speed']            # ground speed
    #    print msp.msp_osd_config['osd_items'][8]
    if msp_cmd == 130:
        print msp.msp_battery_state['current']
    if msp_cmd == 108:
        print msp.msp_attitude['yaw'] #
    #if msp_cmd == 84:
    #    print msp.msp_osd_config['osd_items'][26] # pitch/airspeed override

def is_any_thread_alive(threads):
    return True in [t.is_alive() for t in threads]

msp = pmultiwii.Multiwii(None, "localhost", 5763, True, msp_callback)
try:
    print "starting..."
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=send)
    t1.start()
    t2.start()

    while is_any_thread_alive([t1, t2]):
        time.sleep(0)

except Exception,error:
    print "Error on Main"+ str(error)
