# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import os,sys

#Create Necessary folders and organizes all files on the device

FileList = os.listdir("/")
File_structure = {"/lib":["AS5600.py","fontlib.py","ssd1306_b.py","IRC_Client.py","eeprom_i2c.py","bdevice.py"],
                  "/utils":[],
                  "/fonts":["cellphone (5,7).bmp","icons (5,7).bmp","five (5,5).bmp","futuristic (5,7).bmp","oldschool (5,7).bmp"],
                  "/sprites":["cloudy.bmp","hazy.bmp","mostly_sunny.bmp","partially_cloudy.bmp","rain.bmp","snow.bmp","sunny.bmp","thunder_storm.bmp"]
                  }
folders = ['sprites','fonts','lib','utils']
for folder in folders:
    if not folder in FileList:
        os.mkdir(folder)

    for file in File_structure["/"+folder]:
        if file in FileList:
            print(file,folder+"/"+file)
            os.rename(file, folder+"/"+file)