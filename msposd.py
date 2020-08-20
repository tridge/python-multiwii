#!/usr/bin/env python
# import pygame module in this program 
import pygame
import threading
import time
import sys
import pmultiwii
import math
  
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

message = "ABCDEF"
hide_message = False
stop_bg_task = False
osd_pos = [None] * 60


def msp_callback(msp_cmd, dataSize):
    global message, hide_message, osd_pos
    #print "received cmd " + str(msp_cmd) + ", " + str(dataSize)
    if msp_cmd == 10:
        message = msp.msp_name['name']
    elif msp_cmd == 84: # osd pos
        # pos = 2048 + pos_x*1 + pos_y*32
        for i in range(0, 57):
            pos = msp.msp_osd_config['osd_items'][i][0]
            if pos >= 2048:
                pos_y = math.floor((pos-2048)/32)
                pos_x = pos - (2048+(pos_y*32))
                osd_pos[i] = {pos_x, pos_y}
            else:
                osd_pos[i] = None
        print "msg pos: " + str(osd_pos[OSD_CRAFT_NAME])

def get_data():
    while True:
        global msp
        if stop_bg_task:
            break
        msp.receiveTcpByte()

msp = pmultiwii.Multiwii(None, "localhost", 5763, True, msp_callback)

t1 = threading.Thread(target=get_data, args=())
t1.start()
# activate the pygame library 
# initiate pygame and give permission 
# to use pygame's functionality. 
pygame.init() 
  
# define the RGB value for white, 
#  green, blue colour . 
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
black = (0, 0 ,0)
  
# assigning values to X and Y variable 
X = 800
Y = 400
  
# create the display surface object 
# of specific dimension..e(X, Y). 
display_surface = pygame.display.set_mode((X, Y )) 
  
# set the pygame window name 
pygame.display.set_caption('Show Text') 
  
# create a font object. 
# 1st parameter is the font file 
# which is present in pygame. 
# 2nd parameter is size of the font 
font = pygame.font.Font('freesansbold.ttf', 12) 
  
# infinite loop 
while True : 
  
    # create a text suface object, 
    # on which text is drawn on it. 
    text = font.render(message, True, white, black) 
    
    # create a rectangular object for the 
    # text surface object 
    textRect = text.get_rect()  
    
    screen_x = X/2
    screen_y = Y/2
    # set the center of the rectangular object. 
    textRect.center = (screen_x, screen_y) 
    
    # completely fill the surface object 
    # with white color 
    display_surface.fill(black) 
  
    # copying the text surface object 
    # to the display surface object  
    # at the center coordinate. 
    if osd_pos[OSD_CRAFT_NAME] != None:
        display_surface.blit(text, textRect) 
    
    # Draws the surface object to the screen.   
    pygame.display.update()  
    
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT : 
            # clean up
            stop_bg_task = True
            # quit the program. 
            pygame.quit() 
            quit() 
  
    