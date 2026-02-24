import cv2
import time
import HandTrackingModule as hm
import pyautogui as pg
import numpy as np
import threading

dragging = False # Variable to track dragging state

pg.PAUSE = 0 # No pause between pyautogui commands

#smoothening
smoothening = 4
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Frame rate calculation
pTime = 0
cTime = 0

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

print(cap.get(3), cap.get(4))

# Hand detector (mediapipe) setup
detector = hm.HandDetector(detectionCon=0.6, trackCon=0.5)

# Function to move mouse in a separate thread to avoid blocking
def move_mouse(x, y):
    pg.moveTo(x, y, 0)
def drag_mouse():
    pg.mouseDown()
def click_mouse():
    pg.click()
def click_mission_control():
    pg.hotkey('ctrl', 'up')
    time.sleep(0.3)

# Main loop
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)

    hands = [] # List to hold hand landmarks and types

    for i in range(2): # Loop through both hands
        lmList, handType = detector.findPosition(img, i, draw=False) # Get landmarks and type
        hands.append((lmList, handType)) # Append landmarks and type to hands list

    cv2.rectangle(img, (700, 100), (1200, 500), (255, 0, 255), 2)  # Draw rectangle for mouse movement area

    #Right hand controls mouse movement
    for lmList, handType in hands: # Process each hand
        if len(lmList) != 0 and handType == "Right":
            # Index fingertip coordinates
            x1, y1 = lmList[8][1], lmList[8][2]
            y1_6 = lmList[6][2]  # Index joint coordinates
            cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)  # Draw circle at fingertip

            # Middle fingertip coordinates
            x2, y2 = lmList[12][1], lmList[12][2]
            y2_10 = lmList[10][2] # Middle joint coordinates
            cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)

            # Ring fingertip coordinates
            x3, y3 = lmList[16][1], lmList[16][2]
            y3_14 = lmList[14][2] # Ring joint coordinates
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)

            # Pinky fingertip coordinates
            x4, y4 = lmList[20][1], lmList[20][2]
            y4_18 = lmList[18][2]  # Pinky joint coordinates
            cv2.circle(img, (x4, y4), 10, (0, 0, 255), cv2.FILLED)

            # Convert coordinates to screen size so the mouse can move in the middle of the screen
            XM = np.interp(x1, (700,1200), (0, pg.size().width))
            YM = np.interp(y1, (100,500), (0, pg.size().height))

            if y2 > y2_10 and y3 > y3_14 and y4 > y4_18:
                clocX = plocX + (XM - plocX) / smoothening
                clocY = plocY + (YM - plocY) / smoothening
                move_mouse(pg.size().width - clocX, clocY)
                plocX, plocY = clocX, clocY

        #Left hand controls mouse click
        if len(lmList) != 0 and handType == "Left":
            # Index fingertip coordinates
            x12, y12 = lmList[8][1], lmList[8][2]
            y1_62, x1_62 = lmList[6][2], lmList[6][1]  # Index joint coordinates
            x1_52, y1_52 = lmList[5][1], lmList[5][2] # knuckle coordinates
            cv2.circle(img, (x12, y12), 15, (255, 255, 0), cv2.FILLED)  # Draw circle at fingertip

            # Middle fingertip coordinates
            x22, y22 = lmList[12][1], lmList[12][2]
            x2_102, y2_102 = lmList[10][1], lmList[10][2]  # Middle joint coordinates
            x2_92, y2_92 = lmList[9][1], lmList[9][2] # knuckle coordinates
            cv2.circle(img, (x22, y22), 10, (0, 255, 0), cv2.FILLED)

            # Ring fingertip coordinates
            x32, y32 = lmList[16][1], lmList[16][2]
            x3_142, y3_142 = lmList[14][1], lmList[14][2]  # Ring joint coordinates
            x3_132, y3_132 = lmList[13][1], lmList[13][2] # knuckle coordinates
            cv2.circle(img, (x32, y32), 10, (255, 0, 0), cv2.FILLED)

            # Pinky fingertip coordinates
            x42, y42 = lmList[20][1], lmList[20][2]
            x4_182, y4_182 = lmList[18][1], lmList[18][2]  # Pinky joint coordinates
            x4_172, y4_172 = lmList[17][1], lmList[17][2] # knuckle coordinates
            cv2.circle(img, (x42, y42), 10, (0, 0, 255), cv2.FILLED)

            x02, y02 = lmList[4][1], lmList[4][2]
            y0_22 = lmList[3][2]  # Thumb joint coordinates
            x0_22 = lmList[3][1]  # Thumb joint coordinates
            cv2.circle(img, (x02, y02), 10, (0, 255, 255), cv2.FILLED)

            # Click mouse if index finger and thumb are touching
            cv2.line(img, (x02, y02), (x12, y12), (255, 0, 255), 2)
            length = np.hypot(x12 - x02, y12 - y02)
            if length < 35:
                click_mouse()

            # Show Mission control (on mac)
            cv2.line(img, (x42, y42), (x02, y02), (255, 0, 255), 2)
            length2 = np.hypot(x42 - x02, y42 - y02)
            if length2 < 25:
                click_mission_control()

            # do spiderman gesture to hold down mouse (kinda works)
            if y42 < y4_182 and y12 < y1_62 and y22 > y2_102 and y32 > y3_142:
                if not dragging:
                    pg.mouseDown()
                    dragging = True
                print("spiderman")
            else:
                if dragging:
                    pg.mouseUp()
                    dragging = False

            # Thumbs up: thumb up, other fingers down
            if (
                    y02 < y0_22 and  # Thumb tip above thumb joint
                    y1_52 < y2_92 < y3_132 < y4_172 and  # Knuckle order
                    x12 < x1_62 and  # Index tip left of index knuckle
                    x22 < x2_102 and  # Middle tip left of middle knuckle
                    x32 < x3_142 and  # Ring tip left of ring knuckle
                    x42 < x4_182  # Pinky tip left of pinky knuckle
            ):
                pg.scroll(2)

            # Thumbs down: thumb down, other fingers down
            if (
                    y02 > y0_22 and  # Thumb tip below thumb joint
                    y42 < y32 < y22 < y12 and  # Pinky, ring, middle, index tip order (y-axis)
                    x12 < x1_62 and  # Index tip right of index knuckle
                    x22 < x2_102 and  # Middle tip right of middle knuckle
                    x32 < x3_142 and  # Ring tip right of ring knuckle
                    x42 < x4_182
            ):
                pg.scroll(-2)
                print("thumbs down")


    #Frame rate calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #Frame rate display
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    #image display
    cv2.flip(img, 1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

