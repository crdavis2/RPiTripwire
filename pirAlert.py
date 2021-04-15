import RPi.GPIO as GPIO
import time
import picamera
import pyimgur
from twilio.rest import Client


account_sid ="TWILIO_ACCOUNT_SID" # Put your Twilio account SID here
auth_token ="TWILIO_AUTH_TOKEN" # Put your auth token here
client = Client(account_sid, auth_token)

img_dir = "/home/pi/PythonProjects/RPiSecurityProject/"
img = "cameraCapture.jpg"
txt_msg = "Motion Detected"
clientID = "IMGUR_CLIENT_ID" # Client ID for Imgur
im = pyimgur.Imgur(clientID)

GPIO.setmode(GPIO.BOARD) #Set GPIO to pin numbering
pir1 = 8 #Assign pin 8 to PIR1
pir2 = 10 #Assign pin 10 to PIR2

GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
print ("Sensor initializing . . .")
time.sleep(5) # Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")

while True:
    if (GPIO.input(pir1) == True) and (GPIO.input(pir2) == True):
      with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        #camera.start_preview()
        #time.sleep(2)
        camera.capture(img_dir + img)
      uploaded_image = im.upload_image(img_dir + img, title = txt_msg)
        
      print("Motion Detected!")
      message = client.api.account.messages.create(
          to = "+###########", # Put your cellphone number here
          from_ = "+###########", # Put your Twilio number here
          body = "PIR Detected Movement!",
          media_url = uploaded_image.link)
    else:
      print("No motion detected")
    time.sleep(1)

        
GPIO.cleanup() #reset all GPIO
print ("Program ended")
