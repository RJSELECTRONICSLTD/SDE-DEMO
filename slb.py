#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/pi/SDE-DEMO/Adafruit_Python_GPIO-master')
sys.path.append('/home/pi/SDE-DEMO/Python_ST7789-master')
sys.path.append('/home/pi/SDE-DEMO/DHT11_Python-master')
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import dht11

import ST7789 as TFT
#import datetime
import time
import calendar
from time import sleep
from PIL import Image, ImageDraw, ImageFont, ImageColor
import numpy as np

# Raspberry Pi pin configuration: (BCM code)
RST=23
DC=25
SW=24
encodeA1=20
encodeA2=21

LED=17

Wlamp=19

#paramater setting
encode_val=0
cw_val=0
itemSelect=0
reDraw=0

pic_x=[ 80,165,190,150,110,70, 30, 35]
pic_y=[120,110, 60, 25, 10,25, 60,110]
x_size=[80,40,20,20,20,20,20,40]
y_size=[80,40,40,40,20,40,40,40]

#setting picture file path
picPath='/home/pi/SDE-DEMO/picture/'

exe="GO"

picture_w=40
picture_h=40

#setting GPIO

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use BCM2835
GPIO.setup(LED, GPIO.OUT)

GPIO.setup(Wlamp, GPIO.OUT)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encodeA1, GPIO.IN)
GPIO.setup(encodeA2, GPIO.IN)

SPI_PORT = 0
SPI_DEVICE = 0
SPI_MODE = 0b11
SPI_SPEED_HZ = 40000000


#setting display

disp = TFT.ST7789(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=SPI_SPEED_HZ),
       mode=SPI_MODE, rst=RST, dc=DC, led=LED)

# Initialize display.
disp.begin()

# Clear display.
disp.clear()

# Analogue clock setting
width = 240
height = 204
w = width       # screen width
h = height      # screen height


image0 = Image.new("RGB", (disp.width, disp.height), "WHITE")
draw = ImageDraw.Draw(image0)
disp.display(image0)
# Initial screen (Demonstration for displaying images)

imagex={0:Image.open(picPath+'9.bmp'), 1:Image.open(picPath+'2.bmp'), 2:Image.open(picPath+'3.bmp'), 3:Image.open(picPath+'4.bmp'), 4:Image.open(picPath+'5.bmp'), 5:Image.open(picPath+'exit.bmp'), 6:Image.open(picPath+'7.bmp'), 7:Image.open(picPath+'8.bmp'),}

logo=Image.open(picPath+'logo-1.bmp')
logo_width=logo.size[0]
logo_high=logo.size[1]

#LOGO small to big
for x in range (1,11):
	new_w=logo_width*x/10
	new_h=logo_high*x/10
	pic_locate_x=120-new_w/2
	pic_locate_y=102-new_h/2
	disp.display((logo.resize((new_w,new_h),Image.BILINEAR)),pic_locate_x,pic_locate_y,pic_locate_x+new_w-1,pic_locate_y+new_h-1)
	sleep(0.1)

#LOGO rotation
for x in range (0,361,5):
	new_logo=logo.rotate(x,Image.BILINEAR)
	new_w=new_logo.size[0]
	new_h=new_logo.size[1]
	pic_locate_x=120-new_w/2
	pic_locate_y=102-new_h/2
	disp.display(new_logo,pic_locate_x,pic_locate_y,pic_locate_x+new_w-1,pic_locate_y+new_h-1)
	sleep(0.01)
sleep(1)
# ENCODE READ
def rotation_encode():
	if GPIO.input(encodeA1)==1:
		A1_val=0x10
	else:
		A1_val=0x00
	if GPIO.input(encodeA2)==1:
		A2_val= 0x01
	else:
		A2_val=0x00
	first_val=A1_val or A2_val
	
	sleep(0.01)
	
	if GPIO.input(encodeA1)==1:
		A1_val= 0x10
	else:
		A1_val= 0x00
	if GPIO.input(encodeA2)==1:
		A2_val= 0x01
	else:
		A2_val= 0x00
	second_val=A1_val or A2_val
	cw_val=0
	if first_val!=second_val:
		if first_val==0x00 and second_val==0x10:
			cw_val=-1
		if first_val==0x00 and second_val==0x01:
			cw_val=1
		if first_val==0x10 and second_val==0x11:
			cw_val=-1
		if first_val==0x10 and second_val==0x00:
			cw_val=1
		if first_val==0x11 and second_val==0x01:
			cw_val=-1
		if first_val==0x11 and second_val==0x10:
			cw_val=1
		if first_val==0x01 and second_val==0x00:
			cw_val=-1
		if first_val==0x01 and second_val==0x11:
			cw_val=1
	return cw_val
    
def ovenMode():
    c1=Image.open(picPath+'c1.bmp')
    c2=Image.open(picPath+'c3bmp.bmp')
    c3=Image.open(picPath+'c5bmp.bmp')
    c4=Image.open(picPath+'c7bmp.bmp')
    sleep(0.5)
 
    fontJ = ImageFont.truetype('cmr10.ttf', 24, encoding='unic')
    textimage = Image.new('RGBA', (width, height), (255,255,255))
    textdraw = ImageDraw.Draw(textimage)
   
 
    while GPIO.input(SW)==1:
        disp.display(c1, 80,40,159,159)
        sleep(0.3)
        disp.display(c2, 80,40,159,159)
        sleep(0.3)   
        disp.display(c3, 80,40,159,159)
        sleep(0.3)   
        disp.display(c4, 80,40,159,159)
        sleep(0.3)
    sleep(1)

def carMode():
    car=[Image.open(picPath+'LP.bmp'),Image.open(picPath+'LR.bmp'),Image.open(picPath+'LN.bmp'),Image.open(picPath+'LD.bmp'),Image.open(picPath+'L1.bmp'),Image.open(picPath+'L2.bmp'),Image.open(picPath+'L3.bmp'),Image.open(picPath+'L4.bmp')]
    print("CAR MODE demo 2")
    print(car[0].size[0])
    disp.display(car[0],88,80,169,198)
    r=0
    sleep(0.5)
    while GPIO.input(SW)==1:
        i=rotation_encode()
        if i !=0:
            r=r+i
            if r==-1:
                r=0
            if r==8:
                r=7
            disp.display(car[r],88,80,169,198)
            i=0


def girlDance():
    girl=[Image.open(picPath+'g1.bmp'),Image.open(picPath+'g2.bmp'),Image.open(picPath+'g3.bmp'),Image.open(picPath+'g4.bmp'),Image.open(picPath+'g5.bmp'),Image.open(picPath+'g6.bmp'),Image.open(picPath+'g7.bmp'),Image.open(picPath+'g8.bmp'),Image.open(picPath+'g9.bmp'),Image.open(picPath+'g10.bmp')]
    print("function demo 2")
    sleep(0.5)
    while GPIO.input(SW)==1:
        for i in range(10):
            disp.display(girl[i], 80,80,135,159)
            sleep(0.2)
            
def getTime():
    font1 = ImageFont.truetype('LinBiolinum_K.otf', 18, encoding='unic') 
    font2 = ImageFont.truetype('LinBiolinum_K.otf', 24, encoding='unic')
    sleep(0.5)
    while GPIO.input(SW)==1:
        timeFormat=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        print (timeFormat)
        get_date=timeFormat[0:10]
        get_time=timeFormat[11:19]
        print (get_time)
        print (get_date)
        textimage = Image.new('RGBA', (width, height), (255,255,255))
        textdraw = ImageDraw.Draw(textimage)
        textdraw.text((10,75), get_date, font=font1, fill=(255,0,0))
        textdraw.text((20,120), get_time, font=font2, fill=(0,0,255))
        disp.display(textimage)
    
def getCalendar():
    fontJ = ImageFont.truetype('FreeMono.ttf', 16, encoding='unic')
    sleep(0.5)
    i=1
    calendar.setfirstweekday(6)
    timeFormat=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    get_year=int(timeFormat[0:4])
    get_month=int(timeFormat[5:7])
    #print (get_year,get_month)
    while GPIO.input(SW)==1:
        if i!=0:
            cal = calendar.month(get_year, get_month)
            #print cal
            textimage = Image.new('RGBA', (width, height), (255,255,255))
            textdraw = ImageDraw.Draw(textimage)
            textdraw.text((20,55), cal, font=fontJ, fill=(0,0,255))
            disp.display(textimage)
            i=0
        i=rotation_encode()
        get_month=get_month+i
        if get_month==0:
            get_month=12
            get_year=get_year-1
        if get_month==13:
            get_month=1
            get_year=get_year+1
   
def weather():
    instance = dht11.DHT11(pin=16)
    fontJ = ImageFont.truetype('cmr10.ttf', 24, encoding='unic')
    sleep(0.5)
    while GPIO.input(SW)==1:
        result = instance.read()
        if result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            c=str(result.temperature)
            h=str(result.humidity)
            textimage = Image.new('RGBA', (width, height), (255,255,255))
            textdraw = ImageDraw.Draw(textimage)
            textdraw.text((20,85), "Temperature:"+c+ " C", font=fontJ, fill=(0,0,255))
            textdraw.text((20,115), "Humidity:"+h +" %", font=fontJ, fill=(0,0,255))
            disp.display(textimage)
        else:
            textimage = Image.new('RGBA', (width, height), (255,255,255))
            textdraw = ImageDraw.Draw(textimage)
            textdraw.text((20,85), "No DHT 11", font=fontJ, fill=(0,0,255))
            disp.display(textimage)

def lamp():
    p = GPIO.PWM(Wlamp, 60)  # channel=19 frequency=50Hz
    p.start(0)
    dc=0
    fontJ = ImageFont.truetype('LinBiolinum_K.otf', 48, encoding='unic')
    textimage = Image.new('RGBA', (width, height), (255,255,255))
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((15,100), "0 %", font=fontJ, fill=(0,0,255))
    disp.display(textimage)    
    
    sleep(0.5)
    while GPIO.input(SW)==1:
        i=rotation_encode()
        if i!=0:
            dc=dc+i*10
            if dc<0:
                dc=0
            if dc>100:
                dc=100
            print (dc)
            textimage = Image.new('RGBA', (width, height), (255,255,255))
            textdraw = ImageDraw.Draw(textimage)
            textdraw.text((15,100), str(dc)+" %", font=fontJ, fill=(0,0,255))
            disp.display(textimage)

            p.ChangeDutyCycle(dc)
    p.stop
    

def functionDemo(choise):
    disp.display(image0)
    if choise==0:
        carMode()
    if choise==7:
        ovenMode()
    if choise==4:
        lamp()
    if choise==6:
        girlDance()
    if choise==1:
        getTime()
    if choise==2:
        weather()
    if choise==3:
        getCalendar()
    if choise==5:
        global exe
        exe="exit"    

    global reDraw
    disp.display(image0)
    smallLogo=Image.open(picPath+'shanpu.bmp')    
    disp.display(smallLogo,30,180,89,200)
    reDraw=1
    sleep(0.5)


disp.display(image0)
sleep(0.1)
picturecount=[0,7,6,5,4,3,2,1]
for i in picturecount:
    disp.display((imagex[i].resize((x_size[i],y_size[i]),Image.BILINEAR)),pic_x[i],pic_y[i],pic_x[i]+x_size[i]-1,pic_y[i]+y_size[i]-1)

smallLogo=Image.open(picPath+'shanpu.bmp')    
disp.display(smallLogo,30,180,89,200)

while (exe=="GO"):
    rt_val=rotation_encode()
    print(GPIO.input(SW))
    if GPIO.input(SW)==0:
        functionDemo(itemSelect)
    if rt_val!=0 or reDraw==1:
        itemSelect=itemSelect+rt_val
        if itemSelect>7:
            itemSelect=0
        if itemSelect<0:
            itemSelect=7
        j=itemSelect
        reDraw=0
        print(rt_val,itemSelect,j)
        for i in range(0,8):
            disp.display((imagex[j].resize((x_size[i],y_size[i]),Image.BILINEAR)),pic_x[i],pic_y[i],pic_x[i]+x_size[i]-1,pic_y[i]+y_size[i]-1)
            j=j+1
            if j==8:
                j=0 

GPIO.cleanup()
