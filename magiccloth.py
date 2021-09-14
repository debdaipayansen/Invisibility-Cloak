import cv2
import time
import numpy as np #imported libraries
capture_video = cv2.VideoCapture("sample.mp4") #capturing the video background
time.sleep(2)  #giving time for the camera to boot up , adjust to the enviourment because its to dark and needs time to setup
count = 0 
background = 0 #a variable background displayed when I will have the probe on myself aka the background wall 
for i in range(60): #Capturing the background / the webcam is given 60 iterations to capture the background before I come to webcam
    return_val, background = capture_video.read() #Capturing the Background / capture_video.read returns 2 things image that is captured and return vals (T/F)
    if return_val == False : #return value is false that is not capturing
        continue 
    background = np.flip(background, axis = 1)      
while (capture_video.isOpened()): #isopen is used to forcefully open the wbcam and capture 
    return_val, img = capture_video.read() # capturing image to perform operation on it
    if not return_val : 
        break 
    count = count + 1
    img = np.flip(img, axis = 1) 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # coberting capyured image RGB to HSV (Grey , Black and White format) aka Hue Saturation Value / HSB (Hue Saturation Brightness)
    lower_red = np.array([100, 40, 40])  #using np array and puting the HSV value from hsv model [H , S, V]      
    upper_red = np.array([100, 255, 255]) 
    mask1 = cv2.inRange(hsv, lower_red, upper_red) # hsv is the image taken and in range of lower to upper part if their is any part we are seperating it (here the cloak part )
    lower_red = np.array([155, 40, 40]) 
    upper_red = np.array([180, 255, 255]) # this 2 arrays are made as the red colour have the range / angle  150 to  108 deg as well
    mask2 = cv2.inRange(hsv, lower_red, upper_red) #again checking the hsv / image whether thir is any part within the given range
    mask1 = mask1 + mask2 # if thir is any shade of red between 100 - 100 and 155 to 180 then both will be stored in mask 1
    #morpholigical functions used / morph open basically removes any noise in the input image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations = 2) # np ones creating amtrix of 3x3 having all ones in it and multiply with the unit iterating for 2 times
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1) #dilate is used to smooth the image after removing noise from the image
    mask2 = cv2.bitwise_not(mask1) #bitwise not is used as mask 1 was removing the red / probe part ans storing it while mask 2 have the rst of hsv except the cloak part
    res1 = cv2.bitwise_and(background, background, mask = mask1) # bitwise and is used to segment the color from background and mask 1
    res2 = cv2.bitwise_and(img, img, mask = mask2) #used to substitute the cloak part
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 
    cv2.imshow("INVISIBLE MAN", final_output) # basically displays the final output
    k = cv2.waitKey(10) 
    if k == 27:      # when escape key is pressed the window should shut down and the program should stop
        break
 
