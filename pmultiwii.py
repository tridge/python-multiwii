#!/usr/bin/env python

"""
 author: Alex Apostoli
 based on https://github.com/hkm95/python-multiwii
"""

import struct
import serial
import time
import socket
  
class Multiwii:
    """ Multiwii Serial Protocol """
    OSD_RSSI_VALUE              = 0
    OSD_MAIN_BATT_VOLTAGE       = 1
    OSD_CROSSHAIRS              = 2
    OSD_ARTIFICIAL_HORIZON      = 3
    OSD_HORIZON_SIDEBARS        = 4
    OSD_ITEM_TIMER_1            = 5
    OSD_ITEM_TIMER_2            = 6
    OSD_FLYMODE                 = 7
    OSD_CRAFT_NAME              = 8
    OSD_THROTTLE_POS            = 9
    OSD_VTX_CHANNEL             = 10
    OSD_CURRENT_DRAW            = 11
    OSD_MAH_DRAWN               = 12
    OSD_GPS_SPEED               = 13
    OSD_GPS_SATS                = 14
    OSD_ALTITUDE                = 15
    OSD_ROLL_PIDS               = 16
    OSD_PITCH_PIDS              = 17
    OSD_YAW_PIDS                = 18
    OSD_POWER                   = 19
    OSD_PIDRATE_PROFILE         = 20
    OSD_WARNINGS                = 21
    OSD_AVG_CELL_VOLTAGE        = 22
    OSD_GPS_LON                 = 23
    OSD_GPS_LAT                 = 24
    OSD_DEBUG                   = 25
    OSD_PITCH_ANGLE             = 26
    OSD_ROLL_ANGLE              = 27
    OSD_MAIN_BATT_USAGE         = 28
    OSD_DISARMED                = 29
    OSD_HOME_DIR                = 30
    OSD_HOME_DIST               = 31
    OSD_NUMERICAL_HEADING       = 32
    OSD_NUMERICAL_VARIO         = 33
    OSD_COMPASS_BAR             = 34
    OSD_ESC_TMP                 = 35
    OSD_ESC_RPM                 = 36
    OSD_REMAINING_TIME_ESTIMATE = 37
    OSD_RTC_DATETIME            = 38
    OSD_ADJUSTMENT_RANGE        = 39
    OSD_CORE_TEMPERATURE        = 40
    OSD_ANTI_GRAVITY            = 41
    OSD_G_FORCE                 = 42
    OSD_MOTOR_DIAG              = 43
    OSD_LOG_STATUS              = 44
    OSD_FLIP_ARROW              = 45
    OSD_LINK_QUALITY            = 46
    OSD_FLIGHT_DIST             = 47
    OSD_STICK_OVERLAY_LEFT      = 48
    OSD_STICK_OVERLAY_RIGHT     = 49
    OSD_DISPLAY_NAME            = 50
    OSD_ESC_RPM_FREQ            = 51
    OSD_RATE_PROFILE_NAME       = 52
    OSD_PID_PROFILE_NAME        = 53
    OSD_PROFILE_NAME            = 54
    OSD_RSSI_DBM_VALUE          = 55
    OSD_RC_CHANNELS             = 56
    OSD_CAMERA_FRAME            = 57

    MSP_NAME                 =10
    MSP_OSD_CONFIG           =84
    MSP_IDENT                =100
    MSP_STATUS               =101
    MSP_RAW_IMU              =102
    MSP_SERVO                =103
    MSP_MOTOR                =104
    MSP_RC                   =105
    MSP_RAW_GPS              =106
    MSP_COMP_GPS             =107
    MSP_ATTITUDE             =108
    MSP_ALTITUDE             =109
    MSP_ANALOG               =110
    MSP_RC_TUNING            =111
    MSP_PID                  =112
    MSP_BOX                  =113
    MSP_MISC                 =114
    MSP_MOTOR_PINS           =115
    MSP_BOXNAMES             =116
    MSP_PIDNAMES             =117
    MSP_SERVO_CONF           =120
    MSP_BATTERY_STATE        =130

    MSP_SET_RAW_RC           =200
    MSP_SET_RAW_GPS          =201
    MSP_SET_PID              =202
    MSP_SET_BOX              =203
    MSP_SET_RC_TUNING        =204
    MSP_ACC_CALIBRATION      =205
    MSP_MAG_CALIBRATION      =206
    MSP_SET_MISC             =207
    MSP_RESET_CONF           =208
    MSP_SELECT_SETTING       =210
    MSP_SET_HEAD             =211
    MSP_SET_SERVO_CONF       =212
    MSP_SET_MOTOR            =214


    MSP_BIND                 =241

    MSP_EEPROM_WRITE         =250

    MSP_DEBUGMSG             =253
    MSP_DEBUG                =254


    IDLE = 0
    HEADER_START = 1
    HEADER_M = 2
    HEADER_ARROW = 3
    HEADER_SIZE = 4
    HEADER_CMD = 5
    HEADER_ERR = 6

    PIDITEMS = 10


    def __init__(self, serialPort, ipAddress=None, ipPort=None, useTcp=False, callback=None):

        self.msp_data = {}

        self.msp_name = { 
            'name':None 
            }
        self.msp_ident = {
            'version':None,
            'multiType':None,
            'multiCapability':None
            }
        self.msp_status = {
            'cycleTime':None, 
            'i2cError':None, 
            'present':None, 
            'mode':None
            }
        self.msp_raw_imu = {
            'size':0, 
            'accx':0.0, 
            'accy':0.0, 
            'accz':0.0, 
            'gyrx':0.0, 
            'gyry':0.0, 
            'gyrz':0.0
            }
        self.msp_set_rc = {
            'roll':0, 
            'pitch':0, 
            'yaw':0, 
            'throttle':0, 
            'aux1':0, 
            'aux2':0, 
            'aux3':0, 
            'aux4':0
            }
        self.msp_raw_gps = {
            'GPS_fix':0,
            'GPS_numSat':0,
            'GPS_latitude':0,
            'GPS_longitude':0,
            'GPS_altitude':0,
            'GPS_speed':0
            }
        self.msp_comp_gps = {
            'GPS_distanceToHome':0, 
            'GPS_directionToHome':0, 
            'GPS_update':0
            }
        self.msp_attitude = {
            'roll':0, 
            'pitch':0, 
            'yaw':0
            }
        self.msp_altitude = {
            'alt':0,
            'vspeed':0
            }
        self.msp_rc_tuning = {
            'byteRC_RATE':0, 
            'byteRC_EXPO':0, 
            'byteRollPitchRate':0, 
            'byteYawRate':0, 
            'byteDynThrPID':0, 
            'byteThrottle_MID':0, 
            'byteThrottle_EXPO':0
            }
        self.msp_misc = {
            'intPowerTrigger': 0
            }
        self.msp_osd_config = {
            'feature':None,                # 8
            'video_system':None,           # 8
            'units':None,                  # 8
            'rssi_alarm':None,             # 8
            'cap_alarm':None,              # 16
            'unusaed_1':None,              # 8
            'osd_item_count':None,         # 8
            'alt_alarm':None,              # 16
            'osd_items': [None] * 60,   # x16
            'stats_item_count':None,       # 8
            'stats_items': [None] * 30, # x16
            'timer_count':None,            # 8
            'timer_items': [None] * 10, # 16
            'legacy_warnings':None,        # 16
            'warnings_count':None,         # 8
            'enabled_warnings':None,       # 32
            'profiles':None,               # 8
            'selected_profile':None,       # 8
            'osd_overlay':None,            # 8   
        }
        self.msp_battery_state = {
            'cellCount':0, 
            'capacity':0, 
            'voltage':0, 
            'mah':0, 
            'current':0
        }

        self.inBuf = [None] * 255
        self.p = 0
        self.c_state = Multiwii.IDLE
        self.err_rcvd = False
        self.checksum = 0
        self.cmd = 0
        self.offset=0
        self.dataSize=0
        self.servo = []
        self.mot = []
        self.RCChan = []
        self.byteP = []
        self.byteI = []
        self.byteD = []
        self.confINF = []
        self.byteMP = []

        self.confP = []
        self.confI = []
        self.confD = []


        self.ser = serial.Serial()
        self.ser.port = serialPort
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2

        self.ipAddress = ipAddress
        self.ipPort = ipPort
        self.useTcp = useTcp
        self.cmd_callback = callback

        try:
            if not useTcp:
                self.ser.open()
                print "Waking up board on " + self.ser.port + "..."
                time.sleep(2)
            else:
                # Create a TCP/IP socket
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect the socket to the port where the server is listening
                server_address = (ipAddress, ipPort)
                self.sock.connect(server_address)

        except Exception, error:
            print "\n\nError opening port\n" + str(error) + "\n\n"



    def read32(self):
        value =  (self.inBuf[self.p]&0xff) + ((self.inBuf[self.p+1]&0xff)<<8) + ((self.inBuf[self.p+2]&0xff)<<16) + ((self.inBuf[self.p+3]&0xff)<<24)
        self.p = self.p + 4
        return value
    def read16(self):
        value = (self.inBuf[self.p]&0xff) + ((self.inBuf[self.p+1])<<8)
        self.p = self.p + 2
        return value
    def read8(self):
        value = (self.inBuf[self.p])&0xff
        self.p = self.p + 1
        return value


    def requestMSP (self, msp, payload = [], payloadinbytes = False):

        if msp < 0:
            return 0
        checksum = 0
        bf = ['$', 'M', '<']

        pl_size = 2 * ((len(payload)) & 0xFF)
        bf.append(pl_size)
        checksum ^= (pl_size&0xFF)

        bf.append(msp&0xFF)
        checksum ^= (msp&0xFF)
        if payload > 0:
            if (payloadinbytes == False):
                for c in struct.pack('<%dh' % ((pl_size) / 2), *payload):
                    checksum ^= (ord(c) & 0xFF)
            else:
                for c in struct.pack('<%Bh' % ((pl_size) / 2), *payload):
                    checksum ^= (ord(c) & 0xFF)
        bf = bf + payload
        bf.append(checksum)
        #print "here in requesrMSP"
        #print bf
        return bf


    def sendTcpRequestMSP(self, msp, payloadinbytes = False):
        #print "here in sendRequestMSP"
        data = []
        for i in msp:
            data.append(i)
        #print data
        #print "Data length %d " %(len(data)-6)
        try:
            if payloadinbytes == False:
                b = None
                b = self.sock.send(struct.pack('<3c2B%dhB' % (len(data)-6), *data))
            #b = self.ser.write(struct.pack('<3c3B', *data))
            else:
                b = None
                b = self.sock.send(struct.pack('<3c2B%BhB' % (len(data) - 6), *data))
        except Exception, error:
            print "Error in sendRequestMSP"
            print "("+str(error)+")\n\n"        

    def sendRequestMSP(self, msp, payloadinbytes = False):
        #print "here in sendRequestMSP"
        data = []
        for i in msp:
            data.append(i)
        #print data
        #print "Data length %d " %(len(data)-6)
        try:
            if payloadinbytes == False:
                b = None
                b = self.ser.write(struct.pack('<3c2B%dhB' % (len(data)-6), *data))
            #b = self.ser.write(struct.pack('<3c3B', *data))
            else:
                b = None
                b = self.ser.write(struct.pack('<3c2B%BhB' % (len(data) - 6), *data))
        except Exception, error:
            print "Error in sendRequestMSP"
            print "("+str(error)+")\n\n"        

    def evaluateCommand(self, cmd, dataSize):
        self.msp_data[cmd] = self.inBuf[:dataSize]
        if cmd == Multiwii.MSP_NAME:
            s = ''
            for i in range(0,dataSize,1):
                b = self.read8()
                if b == 0:
                    break
                s += chr(b)
            self.msp_name['name'] = s
        elif cmd == Multiwii.MSP_IDENT:
            self.msp_ident['version'] = self.read8()
            self.msp_ident['multiType'] = self.read8()
            self.read8() # MSP version
            self.msp_ident['multiCapability'] = self.read32()

        elif cmd == Multiwii.MSP_STATUS:
            self.msp_status['cycleTime'] = self.read16()
            self.msp_status['i2cError'] = self.read16()
            self.msp_status['present'] = self.read16()
            self.msp_status['mode'] = self.read32()

        elif cmd == Multiwii.MSP_RAW_IMU:
            self.msp_raw_imu['accx'] = float(self.read16())
            self.msp_raw_imu['accy'] = float(self.read16())
            self.msp_raw_imu['accz'] = float(self.read16())
            self.msp_raw_imu['gyrx'] = float(self.read16())
            self.msp_raw_imu['gyry'] = float(self.read16())
            self.msp_raw_imu['gyrz'] = float(self.read16())
            self.msp_raw_imu['magx'] = float(self.read16())
            self.msp_raw_imu['magy'] = float(self.read16())
            self.msp_raw_imu['magz'] = float(self.read16())
            self.msp_raw_imu['size'] = dataSize

        elif cmd == Multiwii.MSP_SERVO:
            for i in range(0,8,1):
                self.servo.append(self.read16())

        elif cmd == Multiwii.MSP_MOTOR:
            for i in range(0, 8, 1):
                self.mot.append(self.read16())

        elif cmd == Multiwii.MSP_RC:
            for i in range(0, 8, 1):
                self.RCChan.append(self.read16())

        elif cmd == Multiwii.MSP_RAW_GPS:
            self.msp_raw_gps['GPS_fix'] = self.read8()
            self.msp_raw_gps['GPS_numSat'] = self.read8()
            self.msp_raw_gps['GPS_latitude'] = self.read32()
            self.msp_raw_gps['GPS_longitude'] = self.read32()
            self.msp_raw_gps['GPS_altitude'] = self.read16()
            self.msp_raw_gps['GPS_speed'] = self.read16()

        elif cmd == Multiwii.MSP_COMP_GPS:
            self.msp_comp_gps['GPS_distanceToHome'] = self.read16()
            self.msp_comp_gps['GPS_directionToHome'] = self.read16()
            self.msp_comp_gps['GPS_update'] = self.read8()

        elif cmd == Multiwii.MSP_ATTITUDE:
            self.msp_attitude['roll'] = (self.read16())/10
            self.msp_attitude['pitch'] = (self.read16())/10
            self.msp_attitude['yaw'] = self.read16()

        elif cmd == Multiwii.MSP_ALTITUDE:
            self.msp_altitude['alt'] = self.read32()
            self.msp_altitude['vspeed'] = self.read16()

        elif cmd == Multiwii.MSP_ANALOG:
            x = None

        elif cmd == Multiwii.MSP_RC_TUNING:
            self.msp_rc_tuning['byteRC_RATE'] = self.read8()
            self.msp_rc_tuning['byteRC_EXPO'] = self.read8()
            self.msp_rc_tuning['byteRollPitchRate'] = self.read8()
            self.msp_rc_tuning['byteYawRate'] = self.read8()
            self.msp_rc_tuning['byteDynThrPID'] = self.read8()
            self.msp_rc_tuning['byteThrottle_MID'] = self.read8()
            self.msp_rc_tuning['byteThrottle_EXPO'] = self.read8()

        elif cmd == Multiwii.MSP_ACC_CALIBRATION:
            x = None

        elif cmd == Multiwii.MSP_MAG_CALIBRATION:
            x = None

        elif cmd == Multiwii.MSP_PID:
            for i in range(0, 8, 1):
                self.byteP[i] = (self.read8())
                self.byteI[i] = (self.read8())
                self.byteD[i] = (self.read8())
                if (i != 4) and (i != 5) and (i != 6):
                    self.confP[i] = (float(self.byteP[i])/10.0)
                    self.confI[i] = (float(self.byteI[i])/1000.0)
                    self.confD[i] = (float(self.byteD[i]))
            self.confP[4] = (float(self.byteP[4]) / 100.0)
            self.confI[4] = (float(self.byteI[4]) / 100.0)
            self.confD[4] = (float(self.byteD[4]) / 1000.0)
            self.confP[5] = (float(self.byteP[5]) / 10.0)
            self.confI[5] = (float(self.byteI[5]) / 100.0)
            self.confD[5] = (float(self.byteD[5]) / 1000.0)
            self.confP[6] = (float(self.byteP[6]) / 10.0)
            self.confI[6] = (float(self.byteI[6]) / 100.0)
            self.confD[6] = (float(self.byteD[6]) / 1000.0)
        elif cmd == Multiwii.MSP_BOX:
            x = None

        elif cmd == Multiwii.MSP_BOXNAMES:
            x = None

        elif cmd == Multiwii.MSP_PIDNAMES:
            x = None

        elif cmd == Multiwii.MSP_SERVO_CONF:
            x = None

        elif cmd == Multiwii.MSP_MISC:
            self.msp_misc['intPowerTrigger'] = self.read16()
            for i in range(0,4,1):
                self.MConf[i] = (self.read16())
            self.MConf[4] = (self.read32())
            self.MConf[5] = (self.read32())

        elif cmd == Multiwii.MSP_MOTOR_PINS:
            for i in range(0, 8, 1):
                self.byteMP.append(self.read16())

        elif cmd == Multiwii.MSP_DEBUGMSG:
            x = None
        elif cmd == Multiwii.MSP_DEBUG:
            x = None
        elif cmd == Multiwii.MSP_OSD_CONFIG:
            self.msp_osd_config['feature'] = int(self.read8())                # 8
            self.msp_osd_config['video_system'] = self.read8()           # 8
            self.msp_osd_config['units'] = self.read8()                  # 8
            self.msp_osd_config['rssi_alarm'] = self.read8()             # 8
            self.msp_osd_config['cap_alarm'] = self.read16()             # 16
            self.msp_osd_config['unusaed_1'] = self.read8()              # 8
            self.msp_osd_config['osd_item_count'] = self.read8()         # 8
            self.msp_osd_config['alt_alarm'] = self.read16()             # 16
            for i in range(0, self.msp_osd_config['osd_item_count'], 1):
                self.msp_osd_config['osd_items'][i] = self.read16()      # x 16
            self.msp_osd_config['stats_item_count'] = self.read8()       # 8
            for i in range(0, self.msp_osd_config['stats_item_count'], 1):
                self.msp_osd_config['stats_items'][i] = self.read16()    # x 16
            self.msp_osd_config['timer_count'] = self.read8()            # 8
            for i in range(0, self.msp_osd_config['timer_count'], 1):
                self.msp_osd_config['timer_items'][i] = self.read16()    # x 16
            self.msp_osd_config['legacy_warnings'] = self.read16()       # 16
            self.msp_osd_config['warnings_count'] = self.read8()         # 8
            self.msp_osd_config['enabled_warnings'] = self.read32()      # 32
            self.msp_osd_config['profiles'] = self.read8()               # 8
            self.msp_osd_config['selected_profile'] = self.read8()       # 8
            self.msp_osd_config['osd_overlay'] = self.read8()
                        # 8
        elif cmd == Multiwii.MSP_BATTERY_STATE:
            self.msp_battery_state['cellCount'] = self.read8()
            self.msp_battery_state['capacity'] =  self.read16()
            self.msp_battery_state['voltage'] = self.read8()
            self.msp_battery_state['mah'] = self.read16()
            self.msp_battery_state['current'] = self.read16()  

    def parseMspData(self, c):
        if self.c_state == Multiwii.IDLE:
            if c == '$':
                self.c_state = Multiwii.HEADER_START
            else:
                self.c_state = Multiwii.IDLE
        elif self.c_state == Multiwii.HEADER_START:
            if c == 'M':
                self.c_state = Multiwii.HEADER_M
            else:
                self.c_state = Multiwii.IDLE
        elif self.c_state == Multiwii.HEADER_M:
            if c == '>':
                self.c_state = Multiwii.HEADER_ARROW
            elif c == '!':
                self.c_state = Multiwii.HEADER_ERR
            else:
                self.c_state = Multiwii.IDLE
    
        elif self.c_state == Multiwii.HEADER_ARROW or self.c_state == Multiwii.HEADER_ERR:
            self.err_rcvd = (self.c_state == Multiwii.HEADER_ERR)
            #print (struct.unpack('<B',c)[0])
            self.dataSize = ((struct.unpack('<B',c)[0])&0xFF)
            # reset index variables
            self.p = 0
            self.offset = 0
            self.checksum = 0
            self.checksum ^= ((struct.unpack('<B',c)[0])&0xFF)
            # the command is to follow
            self.c_state = Multiwii.HEADER_SIZE
        elif self.c_state == Multiwii.HEADER_SIZE:
            #print (struct.unpack('<B',c)[0])
            self.cmd = ((struct.unpack('<B',c)[0])&0xFF)
            self.checksum ^= ((struct.unpack('<B',c)[0])&0xFF)
            self.c_state = Multiwii.HEADER_CMD
        elif self.c_state == Multiwii.HEADER_CMD and self.offset < self.dataSize:
            #print (struct.unpack('<B',c)[0])
            self.checksum ^= ((struct.unpack('<B',c)[0])&0xFF)
            self.inBuf[self.offset] = ((struct.unpack('<B',c)[0]) & 0xFF)
            self.offset += 1
            #print "self.inBuf..."
            #print self.inBuf[offset-1]
        elif self.c_state == Multiwii.HEADER_CMD and self.offset >= self.dataSize:
            # compare calculated and transferred checksum
            #print "Final step..."
            if ((self.checksum&0xFF) == ((struct.unpack('<B',c)[0])&0xFF)):
                if self.err_rcvd:
                    print "Copter didn't understand the request type"
                else:
                    self.evaluateCommand(self.cmd, self.dataSize)
                    
                    if self.cmd_callback != None:
                        self.cmd_callback(self.cmd, self.dataSize)

                    if not self.useTcp:
                        self.ser.flushInput()
                        self.ser.flushOutput()
            else:
                print '"invalid checksum for command "+((int)(cmd&0xFF))+": "+(checksum&0xFF)+" expected, got "+(int)(c&0xFF))'
                print '"<"+(cmd&0xFF)+" "+(dataSize&0xFF)+"> {");'
                for i in range(0, len(self.dataSize), 1):
                    if (i != 0):
                        print ""
                    print ((self.inBuf[i] & 0xFF))
                print "} ["+(struct.unpack('<B',c)[0])+"]"
                print "String"

            self.c_state = Multiwii.IDLE
            #self.ser.flushOutput()
            #break
    
    def receiveTcpData(self):
        while True:
            c = self.sock.recv(1)
            self.parseMspData(c)

    def processTcpData(self):
        c = self.sock.recv(1)
        self.parseMspData(c)

    def receiveTcpByte(self):
        c = self.sock.recv(1)
        self.parseMspData(c)

    def receiveData(self, cmd):
        while self.ser.inWaiting():
            c = self.ser.read(1)
            self.parseMspData(c)

    def setPID(self):
        self.sendRequestMSP(self.requestMSP(Multiwii.MSP_PID))
        self.receiveData(Multiwii.MSP_PID)
        time.sleep(0.04)
        payload = []
        for i in range(0, Multiwii.PIDITEMS, 1):
            self.byteP[i] = int((round(self.confP[i] * 10)))
            self.byteI[i] = int((round(self.confI[i] * 1000)))
            self.byteD[i] = int((round(self.confD[i])))


        # POS - 4 POSR - 5 NAVR - 6

        self.byteP[4] = int((round(self.confP[4] * 100.0)))
        self.byteI[4] = int((round(self.confI[4] * 100.0)))
        self.byteP[5] = int((round(self.confP[5] * 10.0)))
        self.byteI[5] = int((round(self.confI[5] * 100.0)))
        self.byteD[5] = int((round(self.confD[5] * 10000.0))) / 10

        self.byteP[6] = int((round(self.confP[6] * 10.0)))
        self.byteI[6] = int((round(self.confI[6] * 100.0)))
        self.byteD[6] = int((round(self.confD[6] * 10000.0))) / 10

        for i in range(0, Multiwii.PIDITEMS, 1):
            payload.append(self.byteP[i])
            payload.append(self.byteI[i])
            payload.append(self.byteD[i])
        print "Payload:..."
        print payload
        self.sendRequestMSP(self.requestMSP(Multiwii.MSP_SET_PID, payload, True), True)


    def arm(self):
        timer = 0
        start = time.time()
        while timer < 0.5:
            data = [1500,1500,2000,1000]
            self.sendRequestMSP(self.requestMSP(Multiwii.MSP_SET_RAW_RC,data))
            time.sleep(0.05)
            timer = timer + (time.time() - start)
            start =  time.time()

    def disarm(self):
        timer = 0
        start = time.time()
        while timer < 0.5:
            data = [1500,1500,1000,1000]
            self.sendRequestMSP(self.requestMSP(Multiwii.MSP_SET_RAW_RC,data))
            time.sleep(0.05)
            timer = timer + (time.time() - start)
            start =  time.time()


    def receiveIMU(self, duration):
        timer = 0
        start = time.time()
        while timer < duration:
            self.sendRequestMSP(self.requestMSP(Multiwii.MSP_RAW_IMU))
            self.receiveData(Multiwii.MSP_RAW_IMU)
            if self.msp_raw_imu['accx'] > 32768:  # 2^15 ...to check if negative number is received
                self.msp_raw_imu['accx'] -= 65536 # 2^16 ...converting into 2's complement
            if self.msp_raw_imu['accy'] > 32768:
                self.msp_raw_imu['accy'] -= 65536
            if self.msp_raw_imu['accz'] > 32768:
                self.msp_raw_imu['accz'] -= 65536
            if self.msp_raw_imu['gyrx'] > 32768:
                self.msp_raw_imu['gyrx'] -= 65536
            if self.msp_raw_imu['gyry'] > 32768:
                self.msp_raw_imu['gyry'] -= 65536
            if self.msp_raw_imu['gyrz'] > 32768:
                self.msp_raw_imu['gyrz'] -= 65536
            print "size: %d, accx: %f, accy: %f, accz: %f, gyrx: %f, gyry: %f, gyrz: %f  " %(self.msp_raw_imu['size'], self.msp_raw_imu['accx'], self.msp_raw_imu['accy'], self.msp_raw_imu['accz'], self.msp_raw_imu['gyrx'], self.msp_raw_imu['gyry'], self.msp_raw_imu['gyrz'])
            time.sleep(0.04)
            timer = timer + (time.time() - start)
            start = time.time()


    def calibrateIMU(self):
        self.sendRequestMSP(self.requestMSP(Multiwii.MSP_ACC_CALIBRATION))
        time.sleep(0.01)
