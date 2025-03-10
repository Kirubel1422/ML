import cv2
from os.path import exists
from time import time

# model paths for face-detection and eye-detection
fd_model_path=r"/opt/ML/PAUL_AI/.venv/lib/python3.13/site-packages/cv2/data/haarcascade_frontalface_default.xml"
ed_model_path=r"/opt/ML/PAUL_AI/.venv/lib/python3.13/site-packages/cv2/data/haarcascade_eye.xml"

# check if the models are present
if not exists(fd_model_path) or not exists(ed_model_path):
    print('Model not found')
    exit()

# colors
RED_COLOR=(0,0,255)
BLUE_COLOR=(255,0,0)

# parent window dimensions
PWIN_WIDTH=640
PWIN_HEIGHT=360
PWIN_NAME="MAIN"

# create an instance
cap = cv2.VideoCapture(0)

# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIN_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PWIN_HEIGHT)

# create model objects
face_cascade=cv2.CascadeClassifier(fd_model_path)
eye_cascade=cv2.CascadeClassifier(ed_model_path)

# fps props
fps_pos=(0, 30)
fps_thickness=1
fps_font_scale=1
fps_font_family=cv2.FONT_HERSHEY_COMPLEX
fps=30 # initial value

while True:
    # start of processing
    start_time=time()

    # read frame
    _, frame=cap.read()

    # convert frame to gray for faster computation
    g_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # extract faces using imported model
    faces=face_cascade.detectMultiScale(g_frame, 1.3, 5)

    # put rectangle over each face
    for face in faces:
        face_x, face_y, face_w, face_h = face
        cv2.rectangle(frame, (face_x, face_y), (face_x+face_w, face_y+face_h), BLUE_COLOR, 4)

        # extract eyes using imported model               
        eyes=eye_cascade.detectMultiScale(g_frame[face_y:face_y+face_h, face_x:face_x+face_w], 1.3, 5)
     
        # put rectangle over each eye
        for eye in eyes:
            eye_x, eye_y, eye_w, eye_h = eye
            cv2.rectangle(frame[face_y:face_y+face_h, face_x:face_x+face_w], (eye_x, eye_y), (eye_x+eye_w, eye_y+eye_h), RED_COLOR, 2)
    
    # display fps
    cv2.putText(frame, str(fps), fps_pos, fps_font_family, fps_font_scale, RED_COLOR, fps_thickness)

    # show frame
    cv2.imshow(PWIN_NAME, frame)
    cv2.moveWindow(PWIN_NAME, 0, 0)
    
    # end of processing
    end_time=time()

    # pass time filter
    fps_new = 1/(end_time-start_time)
    fps = int((0.9)*fps + (0.1)*fps_new)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        print('Bye')
        break