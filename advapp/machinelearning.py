import numpy as np
import cv2
import sklearn
import pickle
import os
from django.conf import settings

STATIC_DIR = settings.STATIC_DIR


# face detection
face_detector_model = cv2.dnn.readNetFromCaffe(os.path.join(STATIC_DIR,'models/deploy.prototxt.txt'),
                                               os.path.join(STATIC_DIR,'models/res10_300x300_ssd_iter_140000.caffemodel'))
# feature extraction
face_feature_model = cv2.dnn.readNetFromTorch(os.path.join(STATIC_DIR,'models/openface.nn4.small2.v1.t7'))
# face recognition
face_recognition_model = pickle.load(open(os.path.join(STATIC_DIR,'models/machinelearning_face_person_identity.pkl'),
                                          mode='rb'))
# emotion recognition model
emotion_recognition_model = pickle.load(open(os.path.join(STATIC_DIR,'models/machinelearning_face_emotion.pkl'),mode='rb'))


def pipeline_model(img):
    image = img.copy()
    h,w = img.shape[:2]

    # face detection
    img_blob = cv2.dnn.blobFromImage(img,1,(300,300),(104,177,123),swapRB=False,crop=False)
    face_detector_model.setInput(img_blob)
    detections = face_detector_model.forward()
    
    # machcine results
    machinlearning_results = dict(emotion_name = [])
    try:
        count = 1
        if len(detections) > 0:
            for i , confidence in enumerate(detections[0,0,:,2]):
                if confidence > 0.5:
                    box = detections[0,0,i,3:7]*np.array([w,h,w,h])
                    startx,starty,endx,endy = box.astype(int)

                    cv2.rectangle(image,(startx,starty),(endx,endy),(0,255,0))

                    # feature extraction
                    face_roi = img[starty:endy,startx:endx]
                    face_blob = cv2.dnn.blobFromImage(face_roi,1/255,(96,96),(0,0,0),swapRB=True,crop=False)
                    face_feature_model.setInput(face_blob)
                    vectors = face_feature_model.forward()

                    # EMOTION 
                    emotion_name = emotion_recognition_model.predict(vectors)[0]
                    if emotion_name == []:
                        emotion_name = "happy" # modifying the data model from deep neural networks pickle file
                    machinlearning_results['emotion_name'].append(emotion_name)
                    count += 1
    except:
        pass
    return machinlearning_results