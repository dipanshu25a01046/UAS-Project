import math
import cv2 as cv
import numpy as np

def get_color_name_hsv(h, s, v):

    if s < 50 and v > 50:
        return "grey"
    
    if (h < 10 or h >= 170) and s > 50:
        return "red"
    
    elif 20 <= h <= 35 and s > 50:
        return "yellow"
    
    elif 36 <= h <= 85 and s > 50:
        return "green"
    
    elif 86 <= h <= 125 and s > 50:
        return "blue"
    
    elif 140 <= h <= 169 and s > 50:
        return "pink"
    else:
        return "unknown"

for i in range(1, 11):
    a = str(i) + '.png'
    img = cv.imread(a)
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    g_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
 
    thre_img = cv.threshold(g_img, 120, 255, cv.THRESH_BINARY)[1]
    contours, heirarchy = cv.findContours(thre_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    data = []
    
    for cont in contours:
        eplison = 0.01 * cv.arcLength(cont, True)
        approx = cv.approxPolyDP(cont, eplison, True)
        if cv.contourArea(cont) < 50: 
            continue

        if len(approx) == 3:
            casualty = 2
        elif len(approx) == 4:
            casualty = 1
        elif len(approx) == 10:
            casualty = 3
        elif len(approx) > 5:
            casualty = 0
        else:
            casualty = -1

        M = cv.moments(cont)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            mask = np.zeros(img.shape[:2], dtype="uint8")
            cv.drawContours(mask, [cont], -1, 255, -1)
            mean_hsv = cv.mean(hsv_img, mask=mask)
            h, s, v = int(mean_hsv[0]), int(mean_hsv[1]), int(mean_hsv[2])
            color_name = get_color_name_hsv(h, s, v)

            if casualty >= 0:
                data.append(((cx, cy), casualty, color_name))
    

    #formula for calculating priority score=casualty*emergency/pow(distance,1.5)
