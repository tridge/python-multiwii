#!/usr/bin/env python
# import pygame module in this program 

import pygame
import threading
import time
import sys
import pmultiwii
import math
  
message = "ABCDEF"
hide_message = False
stop_bg_task = False


def msp_callback(msp_cmd, dataSize):
    pass

def get_data():
    while True:
        global msp
        if stop_bg_task:
            break
        msp.receiveTcpByte()

msp = pmultiwii.Multiwii(None, "localhost", 5763, True, msp_callback)

t1 = threading.Thread(target=get_data, args=())
t1.start()

pygame.init()
  
# define the RGB value for white, 
#  green, blue colour . 
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
black = (0, 0 ,0)
  
# window size
FontWidth = 25
FontHeight = 25

WindowWidth = 32 * FontWidth
WindowHeight = 16 * FontHeight
  
# create the display surface object 
# of specific dimension..e(X, Y). 
display_surface = pygame.display.set_mode((WindowWidth,WindowHeight))

# set the pygame window name
pygame.display.set_caption('Show Text') 
  

def item_to_pos(item):
    '''map MSP item to a X,Y tuple or None'''
    if item >= msp.msp_osd_config['osd_item_count']:
        return None
    pos = msp.msp_osd_config['osd_items'][item]
    if pos < 2048:
        return None
    pos_y = (pos-2048) // 32
    pos_x = (pos-2048) % 32
    return (pos_x, pos_y)


def display_text(item,message):
    XY = item_to_pos(item)
    if XY is None:
        return
    (X,Y) = XY
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    
    px = X * FontWidth
    py = Y * FontHeight
    textRect.center = (px, py)
    display_surface.blit(text, textRect)

def display_all():
    '''display all items'''
    display_text(msp.OSD_CURRENT_DRAW, "%.2fA" % (msp.msp_battery_state['current']*0.001))
    display_text(msp.OSD_MAIN_BATT_VOLTAGE, "%.2fV" % (msp.msp_battery_state['voltage']*0.001))
    display_text(msp.OSD_GPS_SPEED, "%.1fm/s" % (msp.msp_raw_gps['GPS_speed']*0.01))
    display_text(msp.OSD_GPS_SATS, "%uS" % (msp.msp_raw_gps['GPS_numSat']))
    display_text(msp.OSD_ALTITUDE, "%.1fm" % (msp.msp_altitude['alt']*0.01))
    display_text(msp.OSD_CRAFT_NAME, "%s" % (msp.msp_name['name']))

font = pygame.font.Font('freesansbold.ttf', 12)

# infinite loop 
while True:
    time.sleep(0.1)

    # completely fill the surface object
    # with white color 
    display_surface.fill(black) 

    display_all()

    # Draws the surface object to the screen.   
    pygame.display.update()  
    
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT : 
            # clean up
            stop_bg_task = True
            # quit the program. 
            pygame.quit() 
            quit() 
