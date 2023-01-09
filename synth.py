#!/usr/bin/env python3
import live
import logging
from serial import Serial
import pygame
import random
from pygame.locals import *
from pygame import *
import time

logging.basicConfig(format="%(asctime)-15s %(message)s")
logging.getLogger("live").setLevel(logging.INFO)

#setting up arduino
serialPort1 = "/dev/cu.usbmodem142101"
serialPort2 = "/dev/cu.usbmodem142201"
serialPort3 = "/dev/cu.usbmodem142301"
serialPort4 = "/dev/cu.usbmodem142401"
reverbFilterSerial = Serial(serialPort1, baudrate=115200)
chorusVocoderSerial = Serial(serialPort2, baudrate=115200)
delayAttackSerial = Serial(serialPort3, baudrate=115200)
erosionOverdriveSerial = Serial(serialPort4, baudrate=115200)

serialAddys = [reverbFilterSerial, chorusVocoderSerial, delayAttackSerial, erosionOverdriveSerial]

#windowWidth = 750
#windowHeight = 750

#get live set
set = live.Set()
set.scan(scan_devices = True)
lastPlayed = time.time()
print(lastPlayed)

#get all the tracks
tracks_with_devices = list(filter(lambda track: len(track.devices), set.tracks))
if len(tracks_with_devices) == 0:
    raise LiveException("Please open a Live set with at least one device")

#start talking!
set.play()

track = set.tracks[0]
device = track.devices[0]
#paramArray = [0,0,0,0,0,0,0,0,0,0,0,0]
pyReverb = device.parameters[1]
pyReverb.value = 0
pyFilter = device.parameters[2]
pyFilter.value = 0.4
pyChorus = device.parameters[3]
pyVocoder = track.devices[2].parameters[15] #0-1
pyDelay = device.parameters[4]
pyAttack = device.parameters[5]
pyOverdrive = track.devices[1].parameters[4] #0-100
pyErosion = track.devices[3].parameters[3]

# Define the dimensions of
# screen object(width,height)
#screen = pygame.display.set_mode((windowWidth, windowHeight))

# Set the caption of the screen
#pygame.display.set_caption('Synth')

# Fill the background colour to the screen
#screen.fill((0,0,0))

#draw the init view
#for i in range(4):
    #x = (((windowWidth)/4) * i) + 100
    #for j in range(3):
        #y = (((windowHeight)/3) * j) + 100
        #if(i == 0 and j == 2):
            #pygameOutline.append(pygame.draw.circle(screen, (78, 212, 245), (x,y), 50, 0))
            #pygameInside.append(pygame.draw.circle(screen, (0, 0, 0), (x,y), 45, 0))
            #pygameInside.append(pygame.draw.circle(screen, (245, 78, 78), (x,y), 40, 0))
            #pygameInside.append(pygame.draw.circle(screen, (0, 0, 0), (x,y), 35, 0))
            #pygameInside.append(pygame.draw.circle(screen, (92, 245, 78), (x,y), 30, 0))
            #pygameInside.append(pygame.draw.circle(screen, (0, 0, 0), (x,y), 25, 0))
            #pygameInside.append(pygame.draw.circle(screen, (245, 78, 242), (x,y), 20, 0))
            #pygameInside.append(pygame.draw.circle(screen, (0, 0, 0), (x,y), 15, 0))
        #else:
            #pygame.draw.circle(screen, (242, 243, 245), (x,y), 50, 0)
            #pygame.draw.circle(screen, (0, 0, 0), (x,y), 45, 0)
# Update the display using flip
#pygame.display.flip()

def changeParam(output, key):
    play = False
    val_list = output.split(",")
    settings = [[0]*4]*2
    str = ""
    if key == 0:
        str = "reverbFilter"
        param1 = pyReverb
        param2 = pyFilter
        settings[0] = [0,0.5,1,1]
        settings[1] = [1,0.8,0.6,0.4]
    if key == 1:
        str = "erosion chorus"
        param1 = pyErosion
        param2 = pyChorus
        settings[0] = [0,0.3,0.9,0.9]
        settings[1] = [0,0.33,0.66,1]
        #settings = [0,30,150,150][0,33,66,100]
    if key == 2:
        str = "delay attack"
        param1 = pyDelay
        param2 = pyAttack
        settings[0] = [0.5,0.7,0.9,0.9]
        settings[1] = [0,0.4,0.5,0.6]
        #settings = [[0,50,86,86][0.7,1.5,2.5,4.2]]
    if key == 3:
        str = "vocoder overdrive"
        param1 = pyVocoder
        param2 = pyOverdrive
        settings[0] = [0,0.5,1, 1]
        settings[1] = [0,33,66,100]
        #settings = [[0,50,100, 100][0,33,66,100]]
    for i in range(len(val_list)):
        if '' not in val_list and '0' not in val_list:
            val = int(val_list[i])
            if val < 150:
                #print(str)
                play = True
                param1.value = settings[0][i % 3] #mod
                param2.value = settings[1][i // 3] #floor division to get row
    if play == True:
        #timeNow = time.time()
        #if(lastPlayed - timeNow > 5):
        track.clips[0].play()
        #lastPlayed = timeNow

while True:

    key = 0
    #byte_str = erosionOverdriveSerial.read_until()
    #read_str = byte_str.decode("utf-8")
    #read_str.replace(" ","")
    #changeParam(read_str, key)
    #key += 1
    #print(str(key) + ": " + read_str)
    for i in serialAddys:
        byte_str = i.read_until()
        read_str = byte_str.decode("utf-8")
        read_str.replace(" ","")
        changeParam(read_str, key)
        key += 1
        #print(str(key) + ": " + read_str)
    #serialAddys[0].flush()
    #time.sleep(0.2)
    #for i in serialAddys:
    #byte_str2 = serialAddys[1].read_until()
    #read_str2 = byte_str2.decode("utf-8")
    #print("2: " + read_str2)
    #serialAddys[1].flush()
    #time.sleep(0.2)
    #for i in range(len(serialAddys)):
        #senseTouched(read_str, i)
        #val_list = read_str.split(",")
    #pygame.display.flip()

    # for loop through the event queue
    #for event in pygame.event.get():
        # Check for QUIT event
        #if event.type == pygame.QUIT:
            #running = False
    #set.wait_for_next_beat()

    #------------------------------------------------------------------------
    # Select a random parameter of a random device
    # (skipping param 0, which is always Device On/Off)
    #------------------------------------------------------------------------
    #device = random.choice(track.devices)
    #parameter = random.choice(device.parameters[1:])
    #parameter.randomise()
