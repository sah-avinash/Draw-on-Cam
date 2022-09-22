
import cv2
import numpy as np

def findColor(img,colorAry,colorVal):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for color in colorAry:
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        if x != 0 and y != 0:
            cv2.circle(imgResult, (x, y), 15, colorVal[colorAry.index(color)], cv2.FILLED)
            newPoints.append([x,y,colorAry.index(color)])
    cv2.imshow(str(color[0]), mask)
    return newPoints
    

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>300:
            cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.2*peri, True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y+h//2

def drawOnCanvas(myPoints, colorVal):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),15,
                   colorVal[point[2]], cv2.FILLED)

colorAry = [[100,177,153,179,255,255],          ## blue                orange 5,107,0, 19,255,255 ----- 83,70,127,143,222,255(blue)
            [12,152,193,36,232,255],            ## yellow
            [40,54,150,86,219,255]]             ## green               green5 7,67,0, 100,255,255 ----- 12,152,193,36,255,255(yellow)

colorVal = [[255,0,0],[0,255,255],[0,255,0]]

myPoints = []                                   ## [x, y, colorId]

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,640)

while True:
    success, frame = cap.read()
    imgResult = frame.copy()
    newPoints = findColor(frame,colorAry,colorVal)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(newPoints) != 0:
        pass
        # drawOnCanvas(myPoints,colorVal)

    cv2.imshow("Draw on Cam",imgResult)
    
    if cv2.waitKey(1) & 0xFF == ord('c'):
        myPoints = []
        
    elif cv2.waitKey(1) & 0xFF == ord(' '):
        cap.release()
        cv2.destroyAllWindows()
        break
