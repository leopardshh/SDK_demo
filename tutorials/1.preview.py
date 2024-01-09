"""
    Function description: 
        Call HAWK_SDK_Lib to get L/R camera image
"""
import PyGs.gs as gs
import cv2
import time
import numpy as np

if __name__ == "__main__":

    # define camera object
    hawk = gs.Camera()
    # define InitParameters object
    init_params = gs.InitParameters()
    ret = hawk.open(init_params)
    print("open device Failed reg=,err=", ret, gs.ERROR_CODE.ERROR)
    if ret == gs.ERROR_CODE.ERROR:
        print("open device Failed")
        exit(0)

    # turn on the camera
    while True:
        ret, frame_read = hawk.grab_rgb(gs.FRAME_GRAB.SIDE_BY_SIDE)
        if not ret:
            continue
        disp_rgb = cv2.resize(frame_read, (1280, 720))
        cv2.imshow('Preview', np.uint8(disp_rgb))
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    # turn off the camera
    hawk.close()
