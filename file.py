import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os
import yagmail

BTN_PIN = 26
LED_PIN = 17
LOG_FILE_NAME = "/home/pi/camera/log_file.txt"

def take_photo(camera):
    file_name = "/home/pi/camera/img_" + str(time.time()) +".jpg"
    camera.capture(file_name)
    return file_name

def update_log_file(photo_file_name):
    with open(LOG_FILE_NAME ,"a") as f:
        f.write(photo_file_name)
        f.write("\n")

def send_email_with_pic(yagmail_client,file_name):
    yagmail_client.send(to ="rakeshozon@gmail.com" ,
                 subject ="Alert message !",
                 contents= "here is the photo taken By pi(Sara) , and location of the emergency :- 192.168.1.10:5000/check-movement",
                 attachments= file_name)
    


#log_file_setup
if os.path.exists(LOG_FILE_NAME):
    os.remove(LOG_FILE_NAME)
    print("LOG file removed")
#email_setup
password = ""
with open("/home/pi/.local/share/.email_password" , "r") as f:
    password = f.read()
yag = yagmail.SMTP("rakesh.raspberrypi@gmail.com" , password)
print("email setup ok ")

#camera setup
camera = PiCamera()
camera.resolution = (720,480)
camera.rotation = 180
print("waiting 2 sec for the setup")
time.sleep(2)
print("camera setup completed")



#gpios setup

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN ,GPIO.OUT)
GPIO.setup(BTN_PIN , GPIO.IN )
print(" GPIO setup completely")


last_pir_state = GPIO.input(BTN_PIN)
movement_timer = time.time()
last_time_pic_taken = 0
minduration = 5.0
time_thresold = 3.0 
try :
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(BTN_PIN)
        if(GPIO.input(BTN_PIN) == 1):
            GPIO.output(LED_PIN,GPIO.HIGH)            
        else:
            GPIO.output(LED_PIN,GPIO.LOW)        
        if last_pir_state == GPIO.LOW and pir_state == GPIO.HIGH:
            movement_timer = time.time()
        if last_pir_state == GPIO.HIGH and pir_state == GPIO.HIGH:
            if time.time() - movement_timer > time_thresold:
                if time.time() - last_time_pic_taken > minduration:
                    print("take photo and  sent to email ")
                    photo_file_name = take_photo(camera)
                    update_log_file(photo_file_name)
                    send_email_with_pic(yag,photo_file_name)
                    last_time_pic_taken = time.time()
        last_pir_state = pir_state

except KeyboardInterrupt:
    GPIO.cleanup()

