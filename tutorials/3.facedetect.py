"""
    Function description: 
        Call HAWK_SDK_Lib to obtain face location information
"""
import cv2
import PyGs.gs as gs
import numpy as np
import time
MAX_DISPARITY = 64
SCALE = 1
if __name__ == "__main__":
    cam = gs.Camera()

    init_params = gs.InitParameters()
    init_params.camera_id = 0
    ret = cam.open(init_params)
    if ret == gs.ERROR_CODE.ERROR:
        print("open device Failed")
        exit(0)

    #face detect
    gs_facedetect = gs.FaceDetection()
    # enable
    gs_facedetect.enable_face_detection(True)

    key = ''
    while key != 113:  # for 'q' key
        ret, imgl = cam.grab_rgb(gs.FRAME_GRAB.LEFT)
        imgl = cv2.resize(imgl, (640, 480))
        gs_facedetect.get_face_detection_result(imgl)
        img_fd_depth = gs_facedetect.grab_face_detection_image()

        cv2.imshow('Face Detect', img_fd_depth)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.close()
    cv2.destroyAllWindows()
