import face_recognition as fr
import cv2
from os.path import exists

# face encoding - known
k_face=r'images/kirub.jpg'

# check known image existence
if not exists(k_face):
    print(f'[!] Known face {k_face} is not found.')
    exit(1)

# constant vars
PRIMARY_COLOR=(0,255,0)
DESTRUCTIVE_COLOR=(0,0,255)
FONT_FAMILY=cv2.FONT_HERSHEY_COMPLEX_SMALL
FONT_SCALE=0.8
FONT_THICKNESS=1
RECT_THICKNESS=3

# create an instance
cap=cv2.VideoCapture(0)

# window props
PWIN_TITLE="MAIN"
PWIN_WIDTH=640
PWIN_HEIGHT=360

# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PWIN_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PWIN_HEIGHT)

# load file to face-recognition and encode
k_face=fr.load_image_file(k_face)
k_face_location=fr.face_locations(k_face)
k_face_encoded=fr.face_encodings(k_face, k_face_location)[0] # 0 index because only one item

# known face names
k_face_encodings=[k_face_encoded]
k_face_names=["Kirubel Mamo"] # because it is imported from file system

while True:
    # read frame
    _,frame=cap.read()

    # process smaller frame to speed up
    small_frame=cv2.resize(frame, (0,0) ,fx=0.5, fy=0.5)

    # convert frame to rgb to work with face recognition library
    uk_RGB=cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # detect all faces and encode
    uk_face_locations=fr.face_locations(uk_RGB)
    uk_face_encodings=fr.face_encodings(uk_RGB,uk_face_locations)

    # iterate over unknown face encodings and locations
    for uk_face_location, uk_face_encoding in zip(uk_face_locations, uk_face_encodings):
        uk_face_top, uk_face_right, uk_face_bottom, uk_face_left = uk_face_location # extract face positions
        
        # scale back
        name="Unknown Person" # default text 
    
        # compare known and unknown face encodings
        matches=fr.compare_faces(k_face_encodings, uk_face_encoding)
        
        # iterate over matches and catch the name
        if True in matches:
            matchIndex=matches.index(True)
            name=k_face_names[matchIndex]

        # draw rectangle
        cv2.rectangle(img=frame,
                      pt1=(uk_face_left*2, uk_face_top*2),
                      pt2=(uk_face_right*2, uk_face_bottom*2),
                      color=DESTRUCTIVE_COLOR,
                      thickness=RECT_THICKNESS
                      )
    
        # put the name at the frame
        cv2.putText(img=frame,
                    org=(uk_face_left*2, uk_face_top*2-20),
                    color=PRIMARY_COLOR, 
                    text=name, 
                    fontFace=FONT_FAMILY, 
                    fontScale=FONT_SCALE, 
                    thickness=FONT_THICKNESS)
    
    # show frame
    cv2.imshow(PWIN_TITLE,frame)
    cv2.moveWindow(PWIN_TITLE,0,0)

    if cv2.waitKey(10) & 0xff == ord('q'):
        print("Bye")
        break