import cv2
import numpy as np

# global variable
evnt=0
release_evnt=0

# window dimensions
PWIN_WIDTH=640
PWIN_HEIGHT=360

# create an instance
cap = cv2.VideoCapture(0)

# set props
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PWIN_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIN_WIDTH)

# mouse event handle
def mouse_click(event, x, y, flags, _):
    global evnt, UP_LFT, UP_RGT, BT_RGT, BT_LFT, release_evnt

    # upper left corner
    if event == cv2.EVENT_LBUTTONDOWN:
        UP_LFT=(x,y)
        evnt=event # event = 1

    # bottom right corner
    if event == cv2.EVENT_LBUTTONUP:
        BT_RGT=(x,y)
        release_evnt=event # event = 4

        # set up-right and bottom-left corner
        UP_RGT=(BT_RGT[0],UP_LFT[1])
        BT_LFT=(UP_LFT[0],BT_RGT[1])
    
    # close window on double left click
    if event == cv2.EVENT_LBUTTONDBLCLK:
        evnt=event # event = 7

# create a named window
WIN_NAME="MAIN"
cv2.namedWindow(WIN_NAME)
cv2.setMouseCallback(WIN_NAME, mouse_click)

# subframe window
SUB_WIN="ROI"
ROI=np.array([])

while True:
    # read frame
    _, frame = cap.read()

    # extract roi
    if evnt == 1 and release_evnt == 4:
        ROI=frame[UP_LFT[1]: BT_LFT[1], UP_LFT[0]: UP_RGT[0]]

    # close on double click
    
    # show frame main frame
    cv2.imshow(WIN_NAME, frame)
    cv2.moveWindow(WIN_NAME, 0, 0)

    # show subframe
    if ROI.size>0:
        cv2.imshow(SUB_WIN, ROI)
        cv2.moveWindow(SUB_WIN, 650, 0)

    if cv2.waitKey(1) & 0xff == ord('q'):
        print('bye')
        break
