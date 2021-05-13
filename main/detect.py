import base64
from io import BytesIO
import numpy as np
import cv2
# import dlib
import imutils
import numpy as np
from PIL import Image
from imutils import face_utils
import mediapipe as mp
from .annotations import  *
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


facemesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

import os

# import cStringIO
import logging,sys
# FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SHAPE_PREDICTOR_FILE = os.path.join(FILE_DIR, 'files/shape_predictor_68_face_landmarks.dat')
# predictor = dlib.shape_predictor(SHAPE_PREDICTOR_FILE)

# detector = dlib.get_frontal_face_detector()
center_coordinates = (120, 50)
radius = 100
color = (255, 255, 255)
thickness = 50


def base64_decode(data):
    format, imgstr = data.split(';base64,')
    return base64.b64decode(imgstr)


def base64_encode(data):
    if data:
        return 'data:image/png;base64,'+ data.decode('utf-8')


def get_face_detect_data(data):
    nparr = np.fromstring(base64_decode(data), np.uint8)
    # print(nparr, file=sys.stderr)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_data = detectImage(img)
    # print(base64_encode(image_data),file=sys.stderr)
    return base64_encode(image_data)
    



drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
def detectImage(image):
    image = imutils.resize(image, width=300,height = 300)
    # w,h,c = image.shape
    # image = cv2.resize(image,(256,256))
    results = facemesh.process(image)

    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        # print(face_landmarks)
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACE_CONNECTIONS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)
    
    
    # image = cv2.resize(image,(w,h))

    # print(results, file=sys.stderr)
    # image = cv2.circle(image, center_coordinates, radius, color, thickness) 

    # rects = detector(image, 1)
    # for (i, rect) in enumerate(rects):
    #     (x, y, w, h) = face_utils.rect_to_bb(rect)
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     cv2.putText(image, "Face".format(i + 1), (x - 10, y - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    if True:
        output = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        buffer = BytesIO()
        img = Image.fromarray(output)
        img.save(buffer, format="png")
        # print(buffer.getvalue(),file=sys.stderr)
        encoded_string = base64.b64encode(buffer.getvalue())
        # print(encoded_string,file=sys.stderr)
        return encoded_string
