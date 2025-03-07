import cv2
import time
import math

# PROPS
WIDTH=640
HEIGHT=360
WINNAME="OPEN-CV"

# Create an instance
cam = cv2.VideoCapture(0)   

# Configure display window
cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# Check instance
if not cam.isOpened():
    print("Camera not found")
    exit()

fps = 0
while True:
    # Start time
    starttime = time.time()

    # Read frame
    _, frame = cam.read()

    # Put circle on middle
    COORD=(int(WIDTH/2), int(HEIGHT/2))
    CIRCLE_RADIUS=150
    CIRCLE_THICKNESS=10
    CIRCLE_COLOR=(125, 125, 125)
    cv2.circle(
                img=frame,
               center=COORD,
               thickness=CIRCLE_THICKNESS,
               radius=CIRCLE_RADIUS,
               color=CIRCLE_COLOR,
               )
    
    # Put a text 
    LABEL="KIRA"
    TEXT_COLOR=(255, 0, 0)
    FONT_FAM=cv2.FONT_HERSHEY_COMPLEX
    FONT_SCALE=1
    TEXT_COORD=(int(WIDTH/2 - 40) , int(HEIGHT/2  + 20))
    cv2.putText(
        img=frame,
        text=LABEL,
        fontScale=FONT_SCALE,
        org=TEXT_COORD,
        color=TEXT_COLOR,
        fontFace=FONT_FAM,
    )

    # Put text - fps
    FPS_FONT_SCALE=1
    FPS_COORD=(10, 30)
    FPS_THICKNESS=2
    FPS_COLOR=(0, 0, 255)
    FPS_LABEL=f"fps: {str(fps)}"
    cv2.putText(
        img=frame,
        text=FPS_LABEL,
        fontScale=FPS_FONT_SCALE,
        fontFace=FONT_FAM,
        org=FPS_COORD,
        thickness=FPS_THICKNESS,
        color=FPS_COLOR
    )

    # Show frame
    cv2.imshow(WINNAME, frame)

    # End time
    endtime = time.time()
    
    # Set fps
    fps = math.floor(1 / (endtime -starttime))

    if cv2.waitKey(1) & 0xff == ord('q'):
        print('Bye')
        break