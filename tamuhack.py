import cv2
import numpy as np 

#ardunio communication part
import serial
import time
arduino_port = 'COM3'
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)

# Open webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([15, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange) 
    gray_blurred = cv2.blur(mask, (20, 20)) 


    contours, _ = cv2.findContours(gray_blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 2500:  # Filter out small contours
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw the bounding box around the ball
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # draw a circle at the center
            center = (x + w // 2, y + h // 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #print((x+w)-x, " --- ", (y+h)-y)
            print(x, y)
            
            x = x - 300
            y = -y + 450
            z = 500 - h
            
            angle_x = 0
            angle_y = 0

            if(x < 0):
                angle_x = -(np.asin(x / (pow(pow(x, 2) + pow(z, 2), (0.5)))) * 180) / 3.14
            else:
                angle_x = -(np.asin(x / (pow(pow(x, 2) + pow(z, 2), (0.5)))) * 180) / 3.14
                
            if(y < 0):
                angle_y = -(np.asin(y / (pow(pow(y, 2) + pow(z, 2), (0.5)))) * 180) / 3.14
            else:
                angle_y = -(np.asin(y / (pow(pow(y, 2) + pow(z, 2), (0.5)))) * 180) / 3.14
                

            message = str(angle_x) + " " + str(angle_y)
            arduino.write((message + '\n').encode())  
            # print(f"Sent: {message}")
            #time.sleep(0.1)  # 10ms delay


            #Optionally, read the Arduino's response
            # response = arduino.readline().decode().strip()
            # if response:
            #     print(f"Arduino says: {response}")
    
    #display
    cv2.imshow('frame', frame) 
    cv2.imshow('mask', mask) 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
