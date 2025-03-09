import cv2

# create an instance
cap = cv2.VideoCapture(0)

# props
PWIDTH_WIN=640 # parent window width
PHEIGHT_WIN=360 # parent window height

# pass props
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PHEIGHT_WIN)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIDTH_WIN)

# window props
PNAME_WIN_NAME='MAIN'
TRACKER_WIN_NAME='TRACKER'

# window x and y position
winx=0
winy=0

# callbacks
# tracker
def move_win_x(x_pos):
    global winx
    winx=x_pos
def move_win_y(y_pos):
    global winy
    winy=y_pos

# resizing
def resize_frame(frame_size):
    global PWIDTH_WIN, PHEIGHT_WIN
    PWIDTH_WIN=frame_size
    PHEIGHT_WIN=int((360*PWIDTH_WIN)/640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PHEIGHT_WIN)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIDTH_WIN)

# tracker window
cv2.namedWindow(TRACKER_WIN_NAME)  
cv2.resizeWindow(TRACKER_WIN_NAME, 400, 120)
cv2.moveWindow(TRACKER_WIN_NAME, 650, 0)
cv2.createTrackbar('X: ', TRACKER_WIN_NAME, 0, 1920-640, move_win_x)
cv2.createTrackbar('Y: ', TRACKER_WIN_NAME, 0, 1080-360, move_win_y)
cv2.createTrackbar('resize: ', TRACKER_WIN_NAME, int(PWIDTH_WIN/2), 640, resize_frame)

while True:
    # read frame
    _, frame = cap.read()

    if PWIDTH_WIN == 0:
        PWIDTH_WIN=640
        PHEIGHT_WIN=360
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PHEIGHT_WIN)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIDTH_WIN)

    # show frame
    cv2.imshow(PNAME_WIN_NAME, frame)
    cv2.moveWindow(PNAME_WIN_NAME, winx, winy)

    if cv2.waitKey(1) & 0xff == ord('q'):
        print('bye')
        break