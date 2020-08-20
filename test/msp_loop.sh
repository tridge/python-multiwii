#!/bin/bash
COUNTER=0
while [  $COUNTER -lt 10 ]; do
  nc localhost 5762 -w 10 < msp_status.raw
#  nc localhost 5762 -w 0 < msp_raw_imu.raw
  let COUNTER=COUNTER+1 
done
