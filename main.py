import falcon
import json
import os
import spidev
import dbus
import commands
from neopixel import *


from waitress import serve

# LED strip configuration:
LED_COUNT      = 3      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

config = json.load(open('./serverConfig.json'))
CurrDirStr = str(os.getcwd());

GlobalPlayerInfo = {
    'mode': 'bluetooth',
    'status': 'Playing',
    'volume': 100,
    'artist': 'DJ Paul Elstak',
    'title': 'Rainbow in the Sky',
    'albumCover': 'https://img.discogs.com/ljTN0VrZXK5e3fh5co4obege7fY=/fit-in/600x518/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-186742-1395703236-4006.jpeg.jpg',
    'totalTime': '309991',
    'currentTime': '239991',
    'elapsedTime': 20,
    'LEDon': True
}

BTData = {"Status": "nodata", "Name": "nodata", "Track": {"Album": "nodata", "NumberOfTracks": 0, "Artist": "nodata", "Title": "nodata", "Genre": "", "Duration": 202999, "TrackNumber": 0}, "Subtype": "Audio Book", "Device": "nodata", "Position": 39952, "Type": "Audio"}

GlobalLedInfo = {
    'r': 255,
    'g': 255,
    'b': 255
}

class InfoClass:
    def on_get(self, req, resp):
        print("TRYING TO GET INFO")
        getBluetoothData(BT_Media_props)

class PauseClass:
    def on_get(self, req, resp):
        print("TRYING TO PAUSE")
        BT_Media_iface.Pause()

class PlayClass:
    def on_get(self, req, resp):
        print("TRYING TO PLAY")
        BT_Media_iface.Play()

# PlayerInfo shows and changes current player info and settings
class PlayerInfo:
    def on_get(self, req, resp):
        UpdateDataHandler()
        resp.body = json.dumps([GlobalPlayerInfo])

    def on_post(self, req, resp):
        global GlobalPlayerInfo
        GlobalPlayerInfo = json.load(req.bounded_stream)
        dataChangeHandler()


# LedInfo shows and changes current RGB
class LedInfo:
    def on_get(self, req, resp):
        resp.body = json.dumps([GlobalLedInfo])

    def on_post(self, req, resp):
        global GlobalLedInfo
        GlobalLedInfo = json.load(req.bounded_stream)
        dataChangeHandler()


# Automatic Index Redirect
class Index:
    def on_get(self, req, resp):
        raise falcon.HTTPMovedPermanently('/index.html')


def start_server(api, config):
    host = config['host']
    port = config['port']
    serve(api, host=host, port=port)
    print('this probably never gets executed, if it does: cry for help')


def add_routes(api):
    api.add_route('/player', PlayerInfo())
    api.add_route('/led', LedInfo())
    api.add_route('/player/pause', PauseClass())
    api.add_route('/player/play', PlayClass())
    api.add_route('/getinf', InfoClass())
    api.add_route('/', Index())
    api.add_static_route('/', CurrDirStr + '/src')

def dataChangeHandler():
    global strip
    global GlobalLedInfo
    SetSTRIPColor(strip, GlobalLedInfo)
    sendVolume(spi)

def sendVolume(spi):
    volume = GlobalPlayerInfo['volume']
    volume = int(volume)


    value_to_send = [volume]
    spi.xfer(value_to_send)
    print('Sending VOLUME through SPI!')


#Gets Bluetooth music information
def getBluetoothData(props):
    Dict = props.GetAll("org.bluez.MediaPlayer1")
    global BTData
    Data = json.dumps(Dict)
    BTData = json.loads(Data)
    #print BTData

#Gets default player Bluetooth address
def getbtaddress():
    output = commands.getstatusoutput('sudo qdbus --system  org.bluez')
    array = output[1].split('\n')
    for ad in array:
        if 'player' in ad:
            return ad

def UpdateDataHandler():
    getBluetoothData(BT_Media_props)
    global BTData
    global GlobalPlayerInfo
    GlobalPlayerInfo['title'] = BTData['Track']['Title']
    GlobalPlayerInfo['artist'] = BTData['Track']['Artist']
    GlobalPlayerInfo['totalTime'] = BTData['Track']['Duration']
    GlobalPlayerInfo['currentTime'] = BTData['Position']
    GlobalPlayerInfo['status'] = BTData['Status']


def SetSTRIPColor(strip, ledinfo):
    R = ledinfo['r']
    G = ledinfo['g']
    B = ledinfo['b']
    print("Setting Color to "+R+":"+G+":"+B)
    color = Color(R,G,B)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

#SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
sendVolume(spi)


#LED SHIT
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
SetSTRIPColor(strip, GlobalLedInfo)


#Define DBUS
bus = dbus.SystemBus()
BTAddress = getbtaddress()
player = bus.get_object('org.bluez', BTAddress)
BT_Media_iface = dbus.Interface(player, dbus_interface='org.bluez.MediaPlayer1')
BT_Media_props = dbus.Interface(player, "org.freedesktop.DBus.Properties")


api = falcon.API()
add_routes(api)
start_server(api, config)
