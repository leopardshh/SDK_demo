"""
    Function description: 
        Call HAWK_SDK_Lib and get the serial number of the camera
"""
import PyGs.gs as gs
import cv2
import numpy as np
import time

if __name__ == "__main__":

    # define camera object
    hawk = gs.Camera()
    # define InitParameters object
    init_params = gs.InitParameters()
    # print the serial number of the camera
    init_params.camera_id = hawk.get_camera_information().serial_number
    print("hello Leopard")
    print(f"The serial number of the camera is：{init_params.camera_id}")