import falcon
import json
import os
from waitress import serve

config = json.load(open('./serverConfig.json'))
CurrDirStr = str(os.getcwd());

GlobalPlayerInfo = {
    'status': 'Playing',
    'volume': 100,
    'artist': 'DJ Paul Elstak',
    'title': 'Rainbow in the Sky',
    'albumCover': 'https://img.discogs.com/ljTN0VrZXK5e3fh5co4obege7fY=/fit-in/600x518/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-186742-1395703236-4006.jpeg.jpg',
    'totalTime': '02:00',
    'currentTime': '00:20',
    'elapsedTime': 20
}

GlobalLedInfo = {
    'r': 255,
    'g': 255,
    'b': 255
}


# PlayerInfo shows and changes current player info and settings
class PlayerInfo:
    def on_get(self, req, resp):
        print(GlobalPlayerInfo)
        resp.body = json.dumps([GlobalPlayerInfo])

    def on_post(self, req, resp):
        global GlobalPlayerInfo
        GlobalPlayerInfo = json.load(req.bounded_stream)
        print(GlobalPlayerInfo)



# LedInfo shows and changes current RGB

class LedInfo:
    def on_get(self, req, resp):
        resp.body = json.dumps([GlobalLedInfo])


# Automatic Index Redirect
class Index:
    def on_get(self, req, resp):
        raise falcon.HTTPMovedPermanently('/index.html')


def start_server(api, config):
    host = config['host']
    port = config['port']
    serve(api, host=host, port=port)


def add_routes(api):
    api.add_route('/player', PlayerInfo())
    api.add_route('/led', LedInfo())
    api.add_route('/', Index())
    api.add_static_route('/', CurrDirStr + '\src')


api = falcon.API()
add_routes(api)
start_server(api, config)
