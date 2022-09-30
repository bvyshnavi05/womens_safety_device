from flask import Flask
import os
import geocoder


CAMERA_PATH = "/home/pi/camera"
LOG_FILE_NAME = CAMERA_PATH + "/log_file.txt"
photo_cntr = 0
g = geocoder.ip('me') #initialising the gps oject

app = Flask(__name__,static_url_path = CAMERA_PATH ,static_folder= CAMERA_PATH )

@app.route("/")
def index():
    return "hello"

@app.route("/check-movement")
def check_movement():
    message= ""
    file_cntr = 0
    last_file_name = ""
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME , "r") as f:
            for line in f:
                file_cntr += 1
                last_file_name = line
        global photo_cntr
        difference = file_cntr - photo_cntr
        message = str(difference) + "is the no of photos since ur last visit <br/></br/>"
        message += "last photo:" + last_file_name + "<br/>"
        message += "the longitude and latitude of the photo taken " + str((g.latlng)) + "<br/>"
        message += "<img src = \"" + last_file_name + "\" >" 
        
        photo_cntr = file_cntr
    else:
        message = "no pic found"
    return message


        
app.run(host ="0.0.0.0")
