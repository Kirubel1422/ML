import cv2

# PROPS
WIN_WIDTH=1080
WIN_HEIGHT=720
PARENT_WIN_NAME="MAIN"
ROI_WIN_NAME="ROI"

# create an instance
cam = cv2.VideoCapture(0)

# set window props
cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIN_WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, WIN_HEIGHT)

# check camera
if not cam.isOpened():
    print('Camera not found')
    exit()

# extensions to the child window
x_span = 240
y_span = 150

# child window intial positions
startX = 0 
startY = 0
endX = WIN_WIDTH - x_span
endY = WIN_HEIGHT - y_span

x_bounce = False
y_bounce = False

while True:
    # read frame
    _, frame = cam.read()
   
    # horizontal movement 
    if startX < endX and not x_bounce:
        startX = startX + 6
    else:
        if startX > 0:
            x_bounce = True
            startX = startX - 6
        else:
            startX = 0
            x_bounce = False

    # vertical movement
    if startY < endY and not y_bounce:
        startY = startY + 5
    else:
        if startY > 0:
            startY = startY - 5
            y_bounce = True
        else:
            y_bounce = False

    # extract roi and this is fixed
    ROI=frame[startY: startY + y_span, startX: startX + x_span]

    # prepare gray frame
    g_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # show frame
    cv2.imshow(PARENT_WIN_NAME, g_frame)
    cv2.moveWindow(PARENT_WIN_NAME, 0, 0)

    # float around ROI
    cv2.imshow(ROI_WIN_NAME, ROI)
    cv2.moveWindow(ROI_WIN_NAME, startX, startY)

    if cv2.waitKey(1) & 0xff == ord('q'):
        print("bye")
        break
