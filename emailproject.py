import cv2
import numpy as np
import time
import os

import smtplib
from email.message import EmailMessage
import imghdr
name = True
files = []

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "Pikachu0304xd@gmail.com"
    msg['from'] = user
    password = "kismreeqtucjsdik"
    
    for file in files:
        with open(file, 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

status = False
#cap = cv2.VideoCapture('vtest.avi')
cap = cv2.VideoCapture(0)
cam = cv2.VideoCapture(0)
ret, Frame1 = cap.read()
ret, Frame2 = cap.read()

try:
    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')
    
currentframe = 0
st=time.time()
ti=st

while cap.isOpened():
    diff = cv2.absdiff(Frame1, Frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    retur, Thres = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilute = cv2.dilate(Thres, None, iterations=3)
    contoures, hire = cv2.findContours(
        dilute, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(Frame1, contoures, -1, (0, 255, 0,), 2)
    
    for contour in contoures:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 5000:
            cv2.rectangle(Frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            status = True
            
            en=time.time()
            # time.sleep(1)
            if en-st>1:
                name = './data/frame' + str(currentframe) + '.jpg'
                print('Creating...' + name)
                
                cv2.imwrite(name, Frame1)
                files.append(name)
                currentframe += 1
                st=en

        else:
            continue
                            
    status = False   
    cv2.imshow("feed", Frame1)
    Frame1 = Frame2   
    ret, Frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
ti=en-ti
text="Time Escaped: "+str(ti)+" seconds \nAll captured pics are:-\n "

email_alert("Project pics", text, "omdhawan02@gmail.com")

cv2.destroyAllWindows
cap.release()

