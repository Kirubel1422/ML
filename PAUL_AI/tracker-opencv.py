import cv2
import numpy as np

# colors
RED_COLOR=(0, 0, 255)

# window props
PWIN_WIDTH=640
PWIN_HEIGHT=360
PWIN_NAME="MAIN"

# create instance
cap = cv2.VideoCapture(0)

# configure parent window
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PWIN_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIN_WIDTH)

# tracker bar
TWIN_NAME="Tracker Bars" # tracker bar window name
cv2.namedWindow(TWIN_NAME) # create tracker window
cv2.resizeWindow(TWIN_NAME, 400, 100)

# tracker bar props
#hue_low=0
hue_low=113

#hue_high=10
hue_high=88

#sat_low=0
sat_low=206

# sat_high=10
sat_high=255

#val_low=0
val_low=170

# val_high=10
val_high=255

# define tracker bar event handlers
def handle_hue_low(val): # hue low event handler
    global hue_low
    hue_low=val

def handle_hue_high(val): # hue high event handler
    global hue_high
    hue_high=val

def handle_sat_low(val): # sat low event handler
    global sat_low
    sat_low=val

def handle_sat_high(val): # sat high event handler
    global sat_high
    sat_high=val

def handle_val_low(val): # val low event handler
    global val_low
    val_low=val

def handle_val_high(val): # val high event handler
    global val_high
    val_high=val

# add tracker bars in window
cv2.createTrackbar('HUE LOW: ', TWIN_NAME, hue_low, 179, handle_hue_low) # create hue low tracker bar
cv2.createTrackbar('HUE HIGH: ', TWIN_NAME, hue_high, 179, handle_hue_high) # create hue high tracker bar
cv2.createTrackbar('SAT LOW: ', TWIN_NAME, sat_low, 255, handle_sat_low) # create sat low tracker bar
cv2.createTrackbar('SAT HIGH: ', TWIN_NAME, sat_high, 255, handle_sat_high) # create sat high tracker bar
cv2.createTrackbar('VAL LOW: ', TWIN_NAME, val_low, 255, handle_val_low) # create val low tracker bar
cv2.createTrackbar('VAL HIGH: ', TWIN_NAME, val_high, 255, handle_val_high) # create val high tracker bar

# masks window props
U_MWIN_NAME="Uncolored mask" #uncolored
U_MWIN_WIDTH=int(PWIN_WIDTH/2)
U_MWIN_HEIGHT=int(PWIN_HEIGHT/2)

C_MWIN_NAME="Colored mask" #colored
C_MWIN_WIDTH=int(PWIN_WIDTH/2)
C_MWIN_HEIGHT=int(PWIN_HEIGHT/2)

while True:
    # read frame
    _, frame = cap.read()
    
    # hsv version of the frame
    HSV_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define lower bound and upper bound for pixels
    lower_bounds=np.array([min(hue_low, hue_high), min(sat_low, sat_high), min(val_low,val_high)])
    upper_bounds=np.array([max(hue_low,hue_high), max(sat_low,sat_high), max(val_low,val_high)])

    # create mask
    u_mask=cv2.inRange(HSV_frame, lower_bounds, upper_bounds)
    c_mask=cv2.bitwise_and(frame, frame, mask=u_mask)

    # find contour
    contours, _ = cv2.findContours(u_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # e.g. contours=[[(x1, y1), (x2,y2), ..., (xn,yn)]]
    for contour in contours:
        # find area to exclude some noises
        area = cv2.contourArea(contour)
        if area >= 200:
           # cv2.drawContours(frame, [contour], 0, RED_COLOR, 4)
           x,y,w,h = cv2.boundingRect(contour)
           cv2.rectangle(frame, (x,y), (x+w, y+h), RED_COLOR, 4)

    # resize masks
    resized_u_mask=cv2.resize(u_mask, (U_MWIN_WIDTH,U_MWIN_HEIGHT))
    resized_c_mask=cv2.resize(c_mask, (C_MWIN_WIDTH,C_MWIN_HEIGHT))

    # show masks
    cv2.imshow(U_MWIN_NAME, resized_u_mask) #uncolored
    cv2.moveWindow(U_MWIN_NAME, 0, 480)

    cv2.imshow(C_MWIN_NAME, resized_c_mask) #colored
    cv2.moveWindow(C_MWIN_NAME, U_MWIN_WIDTH+50, 480)

    # show parent window
    cv2.imshow(PWIN_NAME, frame)
    cv2.moveWindow(PWIN_NAME, 0, 0)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        print('Bye')
        break