"""
    Function description: 
        Call HAWK_SDK_Lib to get Depth\disparity\pseudo and so on.
"""
import PyGs.gs as gs
import cv2
import numpy as np
input_width = 640
input_height = 480

if __name__ == "__main__":
    # choose the VPI or TENSORT mode
    choose = input("Please Choose Depth Mode:\n"
          " 1. VPI\n"
          " 2. TensorRT\n")
    if choose == '1':
        # Confige to VPI
        choose = gs.DEPTH_MODE.VPI
    elif choose == '2':
        # Confige to TensorRT
        choose = gs.DEPTH_MODE.TENSORT
    else:
        print("Invalid choice")
        exit(0)

    # define camera object
    hawk = gs.Camera()

    if hawk.set_depth_mode(choose) == gs.ERROR_CODE.ERROR:
        print("set_depth_mode Failed")
        exit(0)

    # define InitParameters object
    init_params = gs.InitParameters()
    init_params.camera_id = 0
    ret = hawk.open(init_params)
    print("open device Failed reg=,err=", ret, gs.ERROR_CODE.ERROR)
    if ret == gs.ERROR_CODE.ERROR:
        print("open device Failed")
        exit(0)
    # turn on the depth data of the camera
    while True:
        ret, frame_read = hawk.grab_rgb(gs.FRAME_GRAB.LEFT)
        if not ret:
            continue
        # get Depth Data
        if choose == gs.DEPTH_MODE.TENSORT:
            depth_data = hawk.grab_depth_data()
            disp_depth = cv2.resize(depth_data, (1280, 720))
            cv2.imshow('depth', np.uint8(disp_depth))

        # get depth_disparity image
        if choose == gs.DEPTH_MODE.TENSORT:
            depth_disparity = hawk.grab_disparity()
            depth_disparity = cv2.resize(depth_disparity, (input_width, input_height))
            cv2.imshow('depth_disparity', np.uint8(depth_disparity))
        else:
            depth_disparity = hawk.grab_depth_data()
            depth_disparity = cv2.resize(depth_disparity, (1280, 720))
            cv2.imshow('depth_disparity', np.uint8(depth_disparity))

        # get depth pseudo
        depth_pseudo = hawk.grab_depth_pseudo()
        disp_pseudo = cv2.resize(depth_pseudo, (input_width, input_height))
        cv2.imshow('depth_pseudo', np.uint8(disp_pseudo))

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # turn off the camera
    hawk.close()