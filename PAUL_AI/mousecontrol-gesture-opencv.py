import mediapipe as mp 
import cv2
import pyautogui as pag
import numpy as np

# constants
MAX_HANDS=1
MIN_DC=0.5
MIN_TC=0.5
CIRCLE_RADIUS=5
PRIMARY_COLOR=(0,255,0)
DESTRUCTIVE_COLOR=(0,0,255)

# window props
PWIN_WIDTH=640
PWIN_HEIGHT=360
PWIN_TITLE="MAIN"

# create an instance
cap=cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(
    static_image_mode=False, 
    max_num_hands=MAX_HANDS, 
    min_detection_confidence=MIN_DC, 
    min_tracking_confidence=MIN_TC
)

# set window width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIN_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PWIN_HEIGHT)

WIN_WIDTH, WIN_HEIGHT=pag.size()

while True:
    # read frame
    _,frame=cap.read()

    # correct the display by flipping right-to-left    
    frame=cv2.flip(frame, 1)

    # convert to rgb as mp uses RGB
    frame_RGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # process the frame to detect gesture
    results=hands.process(frame_RGB)

    if results.multi_hand_landmarks is not None:
        # both hands
        for hand_landmark in results.multi_hand_landmarks:
            landmark = np.array([(lm.x, lm.y) for lm in hand_landmark.landmark])
            landmark_cv = (landmark * [PWIN_WIDTH, PWIN_HEIGHT]).astype(int) # for opencv
            landmark_mouse = (landmark * [WIN_WIDTH, WIN_HEIGHT]).astype(int) # for screen

            # for left click
            cv2.circle( frame, 
                        (landmark_cv[8][0], landmark_cv[8][1]),
                        CIRCLE_RADIUS,
                        PRIMARY_COLOR,
                        thickness=-1
                        )

            # for right click
            cv2.circle( frame, 
                        (landmark_cv[12][0], landmark_cv[12][1]),
                        CIRCLE_RADIUS,
                        DESTRUCTIVE_COLOR,
                        thickness=-1
                        )
            
            x_mouse, y_mouse = landmark_mouse[8]
            
            if abs(x_mouse - pag.position()[0]) > 15 or abs(y_mouse - pag.position()[1]) > 15:
                pag.moveTo(x_mouse, y_mouse)
               
       
    # show frame
    cv2.imshow(PWIN_TITLE, frame)
    cv2.moveWindow(PWIN_TITLE, 0, 0)

    if cv2.waitKey(10) & 0xff == ord('q'):
        print('Bye')
        break