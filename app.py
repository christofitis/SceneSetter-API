from flask import Flask, jsonify, request
import ledcontroller
import dbconnector
import json
from flask_cors import CORS
import time



app = Flask(__name__)
CORS(app)

@app.route("/")
def find_me():
    responce = jsonify(success=True, name="LivingRoom")
    return responce


@app.route("/start/<sceneid>", methods = ['GET'])
def start(sceneid):
    ledcontroller.initialize_led_strip()
    stop()
    time.sleep(1)
    if request.method == "GET":
        scene = {
                'sceneid': sceneid 
            }
        ledcontroller.start(scene)
    responce = jsonify(success=True)
    return responce


@app.route("/stop")
def stop():
    dbconnector.update_db('UPDATE state SET running = 0 WHERE id = 1;')
    ledcontroller.all_off()
    responce = jsonify(success=True)
    return responce


@app.route("/off")
def run_all_off():
    ledcontroller.all_off()
    return "<p>Scene Setter</p>"


@app.route("/findled/<lednum>")
def find_led(lednum):
    ledcontroller.run_find_led(lednum)
    return ""

@app.route("/settings", methods = ["GET"])
def get_settings():
    if request.method == "GET":
        query = dbconnector.query_db('SELECT num_leds, brightness FROM config;')
        settings = {
            'num_leds': query[0][0],
            'brightness': query[0][1]
        }
        responce = jsonify(settings)
        return responce

@app.route("/settings/update", methods = ["POST"])
def update_settings():
    if request.method == "POST":
        data = json.loads(request.data)
        dbconnector.update_db('UPDATE config SET num_leds = "{}" where id = 1'.format(int(data['num_leds'])))
        responce = jsonify(success=True)
        return responce


@app.route("/scenes", methods = ["GET"])
def get_scenes():
    if request.method == "GET":
        query = dbconnector.query_db('SELECT * FROM scenes;')
        scenes = []
        for scene in query:
            scenes.append({
                'id': scene[0],
                'name': scene[1]
            })
        responce = jsonify(scenes)
        return responce


@app.route("/scenes/create", methods = ["POST"])
def create_scenes():
    if request.method == "POST":
        data = json.loads(request.data)
        dbconnector.update_db('INSERT INTO scenes (name) VALUES ("{}")'.format(data['name']))
        responce = jsonify(success=True)
        return responce


@app.route("/scenes/update", methods = ["POST"])
def update_scenes():
    if request.method == "POST":
        data = json.loads(request.data)
        dbconnector.update_db('UPDATE scenes SET name = "{}" where id = {}'.format(data['name'], data['id']))
        responce = jsonify(success=True)
        return responce


@app.route("/scenes/delete", methods = ["DELETE"])
def delete_scenes():
    if request.method == "DELETE":
        data = json.loads(request.data)
        dbconnector.update_db('DELETE FROM scenes where id = {}'.format(data['id']))
        dbconnector.update_db('DELETE FROM scene_layouts where sceneid = {}'.format(data['id']))
        responce = jsonify(success=True)
        return responce


@app.route("/layouts/<sceneid>", methods = ["GET"])
def get_layouts(sceneid):
    if request.method == "GET":
        layouts = []
        query = dbconnector.query_db('SELECT pattern, start, end, red_on, green_on, blue_on, red_off, green_off, blue_off, crawl_length, move_right, crawl_bounce, speed_max, fade_speed_min, fade_speed_max, fade_speed_multiplier, fade_up_chance_ratio, colors, on_frequency, off_frequency, marquee_num_on, marquee_num_off, brightness, sceneid, id, octives, persistence, lacunarity FROM scene_layouts WHERE sceneid = {};'.format(sceneid))
        for layout in query:
            layouts.append(
                {
                    'pattern': layout[0],
                    'start': layout[1],
                    'end': layout[2],
                    'red_on': layout[3],
                    'green_on': layout[4],
                    'blue_on': layout[5],
                    'red_off': layout[6],
                    'green_off': layout[7],
                    'blue_off': layout[8],
                    'crawl_length': layout[9],
                    'move_right': layout[10],
                    'crawl_bounce': layout[11],
                    'speed_max': layout[12],
                    'fade_speed_min': layout[13],
                    'fade_speed_max': layout[14],
                    'fade_speed_multiplier': layout[15],
                    'fade_up_chance_ratio': layout[16],
                    'colors': layout[17],
                    'on_frequency': layout[18],
                    'off_frequency': layout[19],
                    'marquee_num_on': layout[20],
                    'marquee_num_off': layout[21],
                    'brightness': layout[22],
                    'sceneid': layout[23],
                    'id': layout[24],
                    'octives': layout[25],
                    'persistence': layout[26],
                    'lacunarity': layout[27]
                }
            )

        def sortLayouts(e):
            return int(e['start'])

        layouts.sort(key=sortLayouts)
        responce = jsonify(layouts)
        return responce


@app.route("/layouts/update", methods = ["POST"])
def update_layouts():
    if request.method == "POST":
        data = json.loads(request.data)
        for layout in data:
            dbconnector.update_db('UPDATE scene_layouts SET pattern = ?, start = ?, end = ?, red_on = ?, green_on = ?, blue_on = ?, red_off = ?, green_off = ?, blue_off = ?, crawl_length = ?, move_right = ?, crawl_bounce = ?, speed_max = ?, fade_speed_min = ?, fade_speed_max = ?, fade_speed_multiplier = ?, fade_up_chance_ratio = ?, colors = ?, on_frequency = ?, off_frequency = ?, marquee_num_on = ?, marquee_num_off = ?, brightness = ?, octives = ?, persistence = ?, lacunarity = ? where id = ?', (layout['pattern'], layout['start'], layout['end'], layout['red_on'], layout['green_on'], layout['blue_on'], layout['red_off'], layout['green_off'], layout['blue_off'], layout['crawl_length'], layout['move_right'], layout['crawl_bounce'], layout['speed_max'], layout['fade_speed_min'], layout['fade_speed_max'], layout['fade_speed_multiplier'], layout['fade_up_chance_ratio'], layout['colors'], layout['on_frequency'], layout['off_frequency'], layout['marquee_num_on'], layout['marquee_num_off'], layout['brightness'], layout['octives'], layout['persistence'], layout['lacunarity'], layout['id'],))
        responce = jsonify(success=True)
        return responce
    
@app.route("/layouts/create", methods = ["POST"])
def create_layouts():
    if request.method == "POST":
        data = json.loads(request.data)
        for layout in data:
            dbconnector.update_db("INSERT INTO scene_layouts (sceneid, pattern, start, end, red_on, green_on, blue_on, red_off, green_off, blue_off, crawl_length, move_right, crawl_bounce, speed_max, fade_speed_min, fade_speed_max, fade_speed_multiplier, fade_up_chance_ratio, colors, on_frequency, off_frequency, marquee_num_on, marquee_num_off, brightness, octives, persistence, lacunarity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,?)",  (layout['sceneid'], layout['pattern'], layout['start'], layout['end'], layout['red_on'], layout['green_on'], layout['blue_on'], layout['red_off'], layout['green_off'], layout['blue_off'], layout['crawl_length'], layout['move_right'], layout['crawl_bounce'], layout['speed_max'], layout['fade_speed_min'], layout['fade_speed_max'], layout['fade_speed_multiplier'], layout['fade_up_chance_ratio'], layout['colors'], layout['on_frequency'], layout['off_frequency'], layout['marquee_num_on'], layout['marquee_num_off'], layout['brightness'], layout['octives'], layout['persistence'], layout['lacunarity']))
        responce = jsonify(success=True)
        return responce


@app.route("/layouts/delete", methods = ["DELETE"])
def delete_layouts():
    if request.method == "DELETE":
        data = json.loads(request.data)
        dbconnector.update_db('DELETE FROM scene_layouts where id = {}'.format(data['id']))
        responce = jsonify(success=True)
        return responce


@app.route("/patterndefaults/<pattern>", methods = ["GET"])
def get_pattern_defaults(pattern):
    if request.method == "GET":
        query = dbconnector.query_db('SELECT start, end, red_on, green_on, blue_on, red_off, green_off, blue_off, crawl_length, move_right, crawl_bounce, speed_max, fade_speed_min, fade_speed_max, fade_speed_multiplier, fade_up_chance_ratio, colors, on_frequency, off_frequency, marquee_num_on, marquee_num_off, brightness, octives, persistence, lacunarity FROM pattern_defaults WHERE pattern = "{}";'.format(pattern))
        pattern_defaults = {
            'start': query[0][0],
            'end': query[0][1],
            'red_on': query[0][2],
            'green_on': query[0][3],
            'blue_on': query[0][4],
            'red_off': query[0][5],
            'green_off': query[0][6],
            'blue_off': query[0][7],
            'crawl_length': query[0][8],
            'move_right': query[0][9],
            'crawl_bounce': query[0][10],
            'speed_max': query[0][11],
            'fade_speed_min': query[0][12],
            'fade_speed_max': query[0][13],
            'fade_speed_multiplier': query[0][14],
            'fade_up_chance_ratio': query[0][15],
            'colors': query[0][16],
            'on_frequency': query[0][17],
            'off_frequency': query[0][18],
            'marquee_num_on': query[0][19],
            'marquee_num_off': query[0][20],
            'brightness': query[0][21],
            'octives': query[0][22],
            'persistence': query[0][23],
            'lacunarity': query[0][24],
        }
        responce = jsonify(pattern_defaults)
        return responce
