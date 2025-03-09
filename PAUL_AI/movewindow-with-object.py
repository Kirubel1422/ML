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
TWIN_WIDTH=400
TWIN_HEIGHT=100
cv2.namedWindow(TWIN_NAME) # create tracker window
cv2.resizeWindow(TWIN_NAME, TWIN_WIDTH, TWIN_HEIGHT)

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

# movement of window controller
x_scrn=0
y_scrn=0

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

    # find contour
    contours, _ = cv2.findContours(u_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # e.g. contours=[[(x1, y1), (x2,y2), ..., (xn,yn)]]
    for contour in contours:
        # find area to exclude some noises
        area = cv2.contourArea(contour)
        if area >= 100:
            # cv2.drawContours(frame, [contour], 0, RED_COLOR, 4)
            x_win,y_win,w,h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x_win,y_win), (x_win+w, y_win+h), RED_COLOR, 4)
            
            # linear equation establishes relation between opencv window and screen width and height
            x_scrn=int((1920-PWIN_WIDTH)/PWIN_WIDTH)*(x_win)
            y_scrn=int((1080-PWIN_HEIGHT)/PWIN_HEIGHT)*(y_win)

            # move window to the calculated x and y values
            cv2.moveWindow(PWIN_NAME, x_scrn, y_scrn)

    # show parent window
    cv2.imshow(PWIN_NAME, frame)
    cv2.moveWindow(PWIN_NAME, x_scrn, y_scrn)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        print('Bye')
        break