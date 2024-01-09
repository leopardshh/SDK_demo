"""
    Function Description: 
        Call HAWK_SDK_Lib to obtain the information of the target check
"""
import PyGs.gs as gs
import cv2
import numpy as np
import time

if __name__ == "__main__":

    gs_camera = gs.Camera()

    obj_param = gs.ObjectDetection()
    obj_param.enable_object_detection(True)
    obj_param.object_detection()

    init_params = gs.InitParameters()
    init_params.camera_id = 0
    ret = gs_camera.open(init_params)
    if ret == gs.ERROR_CODE.SUCCESS:
        print("Hello,Leopard")
    else:
        print("Enable object detection : " + ret + ". Exit program.")
        gs_camera.close()
        exit()

    while True:
        ret, frame_read = gs_camera.grab_rgb(gs.FRAME_GRAB.LEFT)
        if not ret:
            continue

        obj_res = obj_param.get_object_detection_result(frame_read)
        disp_objdetect = obj_param.grab_object_detection_image()
        cv2.imshow('object detect', np.uint8(disp_objdetect))

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    gs_camera.close()
    def get_camera_information():
        get_camera_information = gs_camera.get_camera_information()
        camera_id = get_camera_information.camera_id
        print(f"sensor id is {camera_id}")
        camera_number = get_camera_information.serial_number
        print(f"sensor number is {camera_number}")
        camera_mode = get_camera_information.camera_model
        print(f"sensor number is {camera_mode}")

    get_camera_information()



