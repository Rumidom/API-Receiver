import machine
import ssd1306_b
import fontlib
import framebuf
from machine import Pin,ADC,I2C
import time
import urequests as requests
import network


i2c = machine.I2C(scl=machine.Pin(47), sda=machine.Pin(48))
width = 128
height = 64
Xoffset = 30
Yoffset = 24
wifi_list = []
playlists = []

#location and ip data
loc_data = {}
time_data = {}

oled = ssd1306_b.SSD1306_I2C(width, height, i2c)
oled.fill(0)
fnt = fontlib.font("fonts/cellphone (5,7).bmp") # Loads font to ram 
buffer = bytearray((height // 8) * width)
fbuf = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_VLSB)
wlan = network.WLAN(network.STA_IF)

cfile = open("config.txt", "r")
timezonedbkey = cfile.readline().rstrip("\n")
cfile.close()

def displayWeatherCode(fbuf,WeatherCode):
    if WeatherCode == 0:
        fontlib.drawBitmap("sprites/sunny.bmp",Xoffset,Yoffset,fbuf)
    elif WeatherCode == 1:
        fontlib.drawBitmap("sprites/mostly_sunny.bmp",Xoffset,Yoffset,fbuf)
    elif WeatherCode == 2:
        fontlib.drawBitmap("sprites/partially_cloudy.bmp",Xoffset,Yoffset,fbuf)
    elif WeatherCode == 3:
        fontlib.drawBitmap("sprites/cloudy.bmp",Xoffset,Yoffset,fbuf)
    elif WeatherCode >= 45 and WeatherCode <= 48:
        fontlib.drawBitmap("sprites/hazy.bmp",Xoffset,Yoffset,fbuf)

def getIpAndLocation():
    resp = requests.get('http://ip-api.com/json/') 
    return resp.json()

def getdatetime(loc_data,key):
    lat = str(loc_data['lat'])
    lon = str(loc_data['lon'])
    resp = requests.get("http://api.timezonedb.com/v2.1/get-time-zone?key="+key+"&format=json&by=position&lat="+lat+"&lng="+lon)
    return resp.json()

def getweatherdata(loc_data,time_data):
    lat = str(loc_data['lat'])
    lon = str(loc_data['lon'])
    timezone = time_data['zoneName']
    date = time_data['formatted'].split(' ')[0]
    URL = "https://api.open-meteo.com/v1/forecast?latitude="+lat+"&longitude="+lon+"&daily=weather_code,temperature_2m_max,temperature_2m_min&current=weather_code,temperature_2m&timezone=" +timezone+"&start_date="+date+"&end_date="+date
    resp = requests.get(url=URL)
    return resp.json()

def getWaveHeight(lat,lon):
    pass

def connectToWifi(SSID, password):
    wlan.active(True)
    wlan.disconnect()
    if not wlan.isconnected():
        wlan.connect(SSID, password)
        i = 0
        while not wlan.isconnected():
            fbuf.fill(0)
            fontlib.prt("Connecting",Xoffset,Yoffset,1,fbuf,fnt)
            fontlib.prt("."*i,Xoffset,Yoffset+10,1,fbuf,fnt)
            oled.show_buffer(buffer)
            time.sleep(1)
            i += 1
            if i > 10:
                break
        if wlan.isconnected():
            fbuf.fill(0)
            fontlib.prt("Connected.",Xoffset,Yoffset,1,fbuf,fnt)
            fontlib.prt(wlan.ifconfig()[0],Xoffset,Yoffset+10,0,fbuf,fnt)
            oled.show_buffer(buffer)
            return True
        else:
            fbuf.fill(0)
            fontlib.prt("Connection",Xoffset,Yoffset,1,fbuf,fnt)
            fontlib.prt("Failed.",Xoffset,Yoffset+10,1,fbuf,fnt)
            oled.show_buffer(buffer)
            return False
        
for pair in wifi_list:
    SSID, Password = pair
    print(pair)
    if connectToWifi(SSID, Password):
        break
    time.sleep(1)
    
if wlan.isconnected():
    loc_data = getIpAndLocation()
    print(loc_data)
    #fontlib.prt(loc_data['city'],Xoffset,Yoffset+20,1,fbuf,fnt)
    time_data = getdatetime(loc_data,timezonedbkey)
    print(time_data)
    fontlib.prt(time_data['formatted'].split(' ')[1],Xoffset,Yoffset+30,1,fbuf,fnt)
    oled.show_buffer(buffer)
    weather_data = getweatherdata(loc_data,time_data)
    print(weather_data)
    fbuf.fill(0)
    displayWeatherCode(fbuf,weather_data['daily']['weather_code'][0])
    fontlib.prt(str(weather_data['daily']['temperature_2m_max'][0])+"c",Xoffset+40,Yoffset+5,1,fbuf,fnt)
    fontlib.prt(str(weather_data['current']['temperature_2m'])+"c",Xoffset+40,Yoffset+15,1,fbuf,fnt)
    fontlib.prt(str(weather_data['daily']['temperature_2m_min'][0])+"c",Xoffset+40,Yoffset+25,1,fbuf,fnt)
    oled.show_buffer(buffer)
    
while True:
    time.sleep(5)

