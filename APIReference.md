# **Python API Documentation**

The HAWK SDK is your gateway to building powerful applications using HAWK cameras, such as camera control, depth sensing, object detection and more.
For camera app developers, this SDK provides a [Camera](#camera) class as the foundation. It unlocks video, depth data, and camera setting control, streamlining your development process.

## **Modules**
In addtion to the [Camera](#camera) Class, the HAWK SDK empowers developers to unlock the full potential of the HAWK camera for building advanced computer vision applications. Its core strength lies in a rich collection of modular and easy-to-use modules, catering to specific features and functionalities.
- [Camera Control](#camera)
- [Depth Sensing](#camera)
- [Object Detection & Face Detection](#object-detection)

---
---
## **Camera Information**
Initialize the basic camera parameters, set and get the serial number and calibration data. More functions are on the way. It will also be called by the [get_camera_information(self)](#getinformation) function in the main `Camera` class.
### Functions

|     |                                                      |
| --- | ---------------------------------------------------- |
| str | [get_serial_number(self)](#getserial)<br>Returns the serial number |
| None    | [get_calibration_data(self)](#getcalibration)<br>Get the calibration data                                                     |

---
## **Camera**
This class acts as the central hub for communication between the camera and the different features of the SDK.

### Functions
|                   |                                                                                                                                                                                                                                                                                          |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| None              | [close(self)](#close)<br>Close an opened camea                                                                                                                                                                                                                                           |
| ERROR_CODE        | [open (self, init_conf=InitParameters())](#open)<br>Open the HAWK camera from the provided InitPamameters                                                                                                                                                                               |
| CameraInformation | [get_camera_information(self)](#getinformation)<br>Return the CameraInformation like serial number, calibration data...                                                                                                                                                                                    |
| int, int        | [get_resize_picture(self, left, right, input_width, input_height)](#getresizepic)<br>Resize the picture, scale the source and target image dimensions                                                                                                                                                     |
| bool, int         | [grab_rgb(self, int index)](#grabrgb)<br>Return a boolean value, True indicates that the image data stream is read, False indicates that it is not read, and an image data stream.<br>                                                                                                              |
| ERROR_CODE        | [set_depth_mode(self, int mode)](#setdepthmode)<br>We provide two depth modes: Tensort and VPI. They are defined in the `DEPTH_MODE` class. The corresponding mode is passed in to set the depth mode type, and the ERROR_CODE is returned.                                 |
| int               | [grab_depth_data(self)](#grabdepth)<br>According to the mode you set in the `set_depth_mode(self, mode)`, we output the depth map.                                                                                                                                                                     |
| int               | [grab_depth_pseudo(self)](#grabpseudo)<br>According to the `grab_depth_data(self)` , we convert the depth map to a pseudo map.                                                                                                                                                                          |
| None              | [set_camera_gain(self, int gain_value)](#setgain)<br>Input a number and set the camera gain.                                                                                                                                                                                                         |
| None              | [set_camera_exposure(self, int exposure_value)](#setexposure)<br>input a number and set the camera exposure.                                                                                                                                                                                             |
| int               | [get_camera_gain(self)](#getgain)<br>Get the camera gain and output it.                                                                                                                                                                                                                              |
| int               | [get_camera_exposure(self)](#getexposure)<br>Get the camera esposure and output it.                                                                                                                                                                                                                      |
| None              | [set_camera_video_settings(self, int index, int val)](#setsetting)<br>Index is a parameter that can be used to select which camera parameter to set. Currently, the following parameters are supported:  exposure, gain. Val is the parameter that specifies the value to set. |
| int               | [get_camera_settings(self, index)](#getsetting)<br>Index is a parameter that can be used to select which camera parameter to get and returns the value.                                                                                                                                                 |

---
## **Object Detection**
This class is mainly used to implement the Object Detection function.

### Functions

|  |  |
| ---- | ---- |
| None | [enable_object_detection(self, bool enable)](#enableobjectdetection)<br>Enable the object detection function |
| None | [object_detection(self)](#objectdetection)<br>Prepare for object detection by importing the model to be used. |
| int | [get_object_detection_result(self, int image)](#getobjectdetectionresult)<br>Return the object detection results. |
| int | [grab_object_detection_image(self)](#grabobjectdetectionimage)<br>Return the object detection image with bouncing box. |
| int | [grab_object_detection_distance_image](#grabobjectdetectiondistanceimage)<br>Return the object detection image with bouncing box and depth distance. |

---
## **Face Detection**
This class is mainly used to implement the Face Detection function.

### Functions

|  |  |
| ---- | ---- |
| None | [enable_face_detection(self, bool enable)](#enablefacedetection)<br>Enable the face detection function |
| int | [get_face_detection_result(self, int image)](#getfacedetectionresult)<br>Return the face detection results. |
| int | [grab_face_detection_image()](#grabfacedetectionimage)<br>Return face detection image with bouncing box and depth distance. |
| int | [grab_face_detection_distance_image(self, int imgL, int imgR)](#grabfacedetectiondistanceimage)<br>Return face detection image with bouncing box. |

---
---
## **Detailed Description**
### **Camera Information Functions**
---

### <span id="getserial"><b>str get_serial_number( self )</b></span><br>

This function is used to retrieve the serial number of the camera. It first constructs a command `cmd` to communicate with the camera using the `i2ctransfer` tool and read a specified length of data. It then executes the command using the `subprocess.run()` function and captures the output of the command. Next, it stores the retrieved serial number in the class attribute `serial_number` and returns it. If an error occurs during execution, the function catches and prints the error message, then returns `None`.

**Returns**<br>
- serial_number: A processed string representing the camera serial number.

---
### <span id="getcalibration" ><b>None get_calibration( self )</b></span><br>

This function is used to retrieve calibration data and store it in the class attributes.  
It instantiates the `stereo_calibration_lib` class and retrieves calibration data such as intrinsic parameters and distortion parameters for the left and right cameras. Then, it stores the intrinsic parameters (fx, cx, fy, cy) for the left and right cameras, as well as the distortion parameters (k1, k2, p1, p2, k3, k4, k5, k6) for both cameras, into the already initialized attributes of the class.

---
### **Camera Functions**
---
### <span id="close"><b> None close (  self ) </b></span><br>

Close an opened camera. We have a [open()](#open) method, if [open()](#open) wasn't called or failed, this method won't work. If [open()](#open) was called, this method will close the camera and free the corresponding memory.

---
### <span id="open"><b> ERROR_CODE  open ( self, init_conf=InitParameters() ) </b></span><br>

Opens the HAWK camera from the provided InitParameters. 
 
**Parameters**
- init_conf: A structure containing all the initial parameters. 

**Returns**
- ERROR_CODE: if the returned error code is ERROR_CODE.SUCCESS, it means the camera is ready for use. Any other code signifies an error, requiring the program to halt.

 Here is a proper way to call this function: 
```
cam = gs.Camera() # Create a HAWK camera object

init_params = gs.InitParameters() # Set configuration parameters
init_params.camera_id = 0
init_params.camera_ae = 1

# Open the camera
ret = cam.open(init_params)
if ret == gs.ERROR_CODE.ERROR:
	print("open device Failed")
	exit(0)
```

---
### <span id="getinformation"><b> CameraInformation   get_camera_information(self) </b></span><br>

Returns the CameraInformation associated the camera being used.

**Returns**
- CameraInformation: containing the hardware parameters of the HAWK, like serial number, calibration data.

---
### <span id="getresizepic"><b> int, int get_resize_picture(self, int left, int right, int input_width, int input_height)</b> </span><br>

Accepting the dimensions of the input left and right video sources as well as the desired target dimensions for resizing, this function utilizes OpenCV's `cv2.resize()` function to adjust the dimensions of the input video sources to the specified target dimensions, returning them as left_resize and right_resize.

**Parameters**
- left, right, input_width, input_height: the dimensions of the input left and right video sources and  the desired target dimensions for resizing

**Returns**
- left_resize and right_resize: resized video data.

---
### <span id="grabrgb"><b> bool, int grab_rgb(self, int index)</b></span><br>

Read images from the left and right cameras, and select to return either the left image, the right image, or a side-by-side concatenation of the two images based on the value of the index.

**Parameters**
- index: According to the class `FRAME_GRAB`, left is 0, right is 1, side-by-side is 2

**Returns**
- image: reaed imge by read(),and then returned.
	
 Here is a proper way to call this function: 
```
def update_frame(self):
	ret_left, frame_left = cam.grab_rgb(gs.FRAME_GRAB.LEFT)
	ret_right, frame_right = cam.grab_rgb(gs.FRAME_GRAB.RIGHT)
	ret_side_by_side, frame_side_by_side = cam.grab_rgb(gs.FRAME_GRAB.SIDE_BY_SIDE)
```

---
### <span id="setdepthmode"><b> ERROR_CODE  set_depth_mode(self, int mode)</b> </span><br>

Initialize some parameters and selects one of the two depth modes: VPI or TENSORT. It loads the model accordingly. If the mode selection fails, it outputs an error code.

**Parameters**
- mode:  According to the class DEPTH_MODE, TENSORT is 0 and VPI is 1.

**Returns**
- ERROR_CODE: if the returned error code is ERROR_CODE.SUCCESS, it means the depth mode is set well. Any other code signifies an error, depth mode will be failed.

 Here is a proper way to call this function: 
```
# set depth mode
if cam.set_depth_mode(gs.DEPTH_MODE.TENSORT) == gs.ERROR_CODE.ERROR:
	print("set_depth_mode Failed")
	exit(0)
```
---
### <span id="grabdepth"><b> int  grab_depth_data(self)</b> </span><br>

This function first preprocesses the frames and then performs different operations based on the selected depth mode that you set in the function [set_depth_mode(self, int mode)](#setdepthmode). If the depth mode is TENSORT, it obtains the disparity map, calculates the depth information based on the disparity map, and returns the result. If the depth mode is VPI, it converts the resized left and right images to the VPI image format, uses the VPI library to compute the disparity map, calculates the depth information based on the disparity map, performs some post-processing, and finally returns the result.

**Returns**
- depth_data: It returns the depth data according to the mode you choose. If no supported depth mode is selected, it returns None.

 Here is a proper way to call this function: 
 ```
# set depth mode
if cam.set_depth_mode(gs.DEPTH_MODE.TENSORT) == gs.ERROR_CODE.ERROR:
	print("set_depth_mode Failed")
	exit(0)
#grab depth data
depth_data = cam.grab_depth_data()
```
---
### <span id="grabpseudo"><b>int grab_depth_pseudo(self)</b> </span><br>

This function performs different operations based on the selected depth mode that you set in the function [set_depth_mode(self, int mode)](#setdepthmode). If the depth mode is TENSORT, it calls a function named `vid_disparity()` in the TENSORT module to convert the disparity map to a pseudo-depth map and returns the result. If the depth mode is VPI, it uses the OpenCV library to apply a color map to the disparity map, converting it to a pseudo-depth map, and returns the result.

**Returns**
- depth_pseudo: It returns the pseudo data according to the mode you choose.  If no supported depth mode is selected, it returns None.
	
 Here is a proper way to call this function: 
 ```
# set depth mode
if cam.set_depth_mode(gs.DEPTH_MODE.TENSORT) == gs.ERROR_CODE.ERROR:
	print("set_depth_mode Failed")
	exit(0)
#grab pseudo data
pseudo_data = cam.grab_depth_pseudo()
```
---
### <span id="setgain"><b> None set_camera_gain(self, int gain_value)</b> </span><br>

This function is used to set the gain value of the cameras. It takes a parameter `gain_value`, which represents the gain value to be set. Then, it constructs two commands, each for setting the gain value of the left and right cameras respectively. These commands are executed in the shell using the `subprocess.run()` function. It will be integrated into the [set_camera_video_settings(self, int index, int val)](#setsetting) function.

**Parameters**
- gain_value: containing the gain parameters.

---
### <span id="getgain"><b> int get_camera_gain(self)</b> </span><br>

This function uses the `subprocess.check_output()` function to execute a command for querying the camera gain value in the shell, then extracts and returns the obtained value.  It will be integrated into the [get_camera_video_settings(self, int index)](#getsetting) function.

**Returns**
- gain_value: containing the gain parameters.

---
### <span id="setexposure"><b> None  set_camera_exposure(self, int exposure_value)</b> </span> <br>

This function is used to set the exposure value of the cameras. It takes a parameter `exposure_value`, which represents the exposure value to be set. Then, it constructs two commands, each for setting the exposure value of the left and right cameras respectively. These commands are executed in the shell using the `subprocess.run()` function. It will be integrated into the [set_camera_video_settings(self, int index, int val)](#setsetting) function.

**Parameters**
- exposure_value: containing the exposure parameters.

---
### <span id="getexposure" ><b> int get_camera_exposure(self) </b></span><br>

This function uses the `subprocess.check_output()` function to execute a command for querying the camera exposure value in the shell, then extracts and returns the obtained value.  It will be integrated into the [get_camera_video_settings(self, int index)](#getsetting) function.

**Returns**
- exposure_value: containing the exposure parameters.

---
### <span id="setsetting" ><b> None  set_camera_video_settings(self, int index, int val) </b></span> <br>

This function is used to set some parameters of the camera, such as exposure and gain. It first checks the value of the index to determine which video property to set, and then calls the corresponding private method to set the exposure or gain of the camera. Before calling the corresponding setting method, it also checks whether the current property value is the same as the value to be set to avoid unnecessary setting operations.

**Parameters**
- index:   From the class `VIDEO_SETTINGS`, BRIGHTNESS is 0, GAIN is 1, CONTRAST is 2, SHARPNESS is 3, EXPOSURE is 4, WHITEBALANCE is 5, HUE is 6, SATURATION is 7, AEC_AGC_ROI is 8, and LED_ON is 9.
- val: Values of the corresponding parameters you want to set.

---
### <span id="getsetting" ><b> int get_camera_video_settings(self, int index)</b> </span><br>

This function is used to retrieve the parameter values of the camera settings. It takes a parameter `index`, which indicates the video property to be retrieved. The function first determines the video property to be retrieved based on the value of `index`, and then calls the corresponding method to retrieve the value of that property. Finally, it returns the retrieved value.

**Parameters**
- index:   From the class `VIDEO_SETTINGS`, BRIGHTNESS is 0, GAIN is 1, CONTRAST is 2, SHARPNESS is 3, EXPOSURE is 4, WHITEBALANCE is 5, HUE is 6, SATURATION is 7, AEC_AGC_ROI is 8, and LED_ON is 9.

**Returns**
- val: Values of the corresponding parameters you want to get.

Here is a proper way to call `set_camera_video_settings(self, int index, int val)` and `get_camera_video_settings(self, int index)`: 
```
#update the setting and show the value
def update_camera_settings(self, value, setting_type, label):
	value = value * 100
	self.cam.set_camera_video_settings(setting_type, value)
	current_value = self.cam.get_camera_settings(setting_type)
	current_value = current_value / 100
	label.setText(f"{setting_type}: {current_value}")
```
---
### Object Detection Functions
---
### <span id="enableobjectdetection" ><b> None enable_object_detection(self, bool enable)</b> </span> <br>

Initializes and starts object detection module.

---
### <span id="objectdetection" ><b> None object_detection(self) </b></span><br>
  
This function is used for object detection. It first checks whether object detection functionality is enabled. If enabled, it loads a model and stores it in the class's `model` attribute. If object detection functionality is not enabled, it prints the corresponding message.

Here is a proper way to call this fucntion.
```
 # enable
 gs_objectdetect = gs.ObjectDetection()
 gs_objdetect.enable_object_detection(True)
 # prepare for object detection by importing the model to be used
 gs_objdetect.object_detection()
```
---
### <span id="getobjectdetectionresult" ><b> int get_object_detection_result(self, int image) </b></span><br>

This function is used to retrieve the results of object detection. It first preprocesses the image, then calls functions in the depth model for object calibration, detection and parsing. Finally, it stores the results in the `detect_result` attribute.

**Parameters**
- image: The image data obtained from the [grab_rgb(self, int index)](#grabrgb) function in the `Camera`.

**Returns**
- detect_result: The results, after calibration, detection, and parsing through the depth model, are stored in the `detect_result` attribute.

---
### <span id="grabobjectdetectionimage" ><b> int get_object_detection_image(self)</b> </span><br>

The purpose of this function is to draw predicted bounding boxes on the image using functions from the depth model, with the `detect_result` attribute obtained from [get_object_detection_result(self, image)](#getobjectdetectionresult).

**Returns**
- detect_img: The image data with the added predicted bounding boxes.

---
### <span id="grabobjectdetectiondistanceimage" > <b>int grab_object_detection_distance_image(self, int depth)</b> </span><br>

The purpose of this function is to draw predicted bounding boxes and distance on the image using functions from the depth model, with the `detect_result` attribute obtained from [get_object_detection_result(self, image)](#getobjectdetectionresult).

**Parameters**
- depth: The depth data obtained from [grab_depth_data(self)](#grabdepth).

**Returns**
- detect_img: The image data with the added bounding boxes and distance.

Here is a proper way to call `get_object_detection_result(self, int image)` and `get_object_detection_image(self)` and `grab_object_detection_distance_image(self, int depth)`:
```
def update_frame(self):
	# Original video
	ret, img = cam.grab_rgb(gs.FRAME_GRAB.LEFT)
	#get object detection result
	object_result =   gs_objectdetect.get_object_detection_result(img)
	#get obejct detection image with bouncing box
	image_objdetect =  gs_objectdetect.grab_object_detection_image()
	#get obejct detection image with bouncing box and distance 
	iamge_distance_objdetect =  gs_objectdetect.grab_object_detection_distance_image()
```

---
### Face Detection Functions
---
### <span id="enablefacedetection" ><b> None enable_face_detection(self, bool enable)</b> </span><br>
Initializes and starts object detection module.

```
#face detect
gs_facedetect = gs.FaceDetection()
# enable
gs_facedetect.enable_face_detection(True)
```
---
### <span id="getfacedetectionresult" ><b> int get_face_detection_result(self, int image)</b> </span><br>

This function is for obtaining face detection results. It preprocesses the image and utilizes a trained face detection model `faceCascade` to detect faces in the image. During the detection process, various parameters can be adjusted, such as the scale factor, minimum neighbors, and minimum size. After detection, the detected face locations are stored in the `detect_result` attribute and returned.

**Parameters**
- int image: The image data obtained from the [grab_rgb(self, int index)](#grabrgb) function in the class `Camera`.

**Returns**
- int detect_result: The detected face locations, after calibration, detection, and parsing through the face detection model, are stored in the `detect_result` attribute.

---
### <span id="grabfacedetectionimage" ><b> int get_face_detection_image(self)</b> </span><br>

This function iterates through each face location information in `detect_result` and utilizes the `cv2.rectangle()` function to draw a rectangle on the image to mark each detected face. After drawing, it returns the image with the face rectangles.

**Returns**
- detect_img: The image data with the added bounding boxes.

---
### <span id="grabfacedetectiondistanceimage" ><b> int grab_face_detection_distance_image(self, int imgL, int imgR) </b></span> <br>

The purpose of this function is to perform face detection while simultaneously calculating the distance between the detected faces and the camera. It then draws bounding boxes around the detected faces on the image and adds corresponding distance information. The entire process involves multiple steps including image preprocessing, computing stereo disparity, face detection, and distance calculation. 

**Parameters**
- imgL, ImgR: The image data obtained from [grab_rgb(self, int index)](#grabrgb) .

**Returns**
- detect_img: The image data with the bounding boxes around the detected faces along with distance information.

Here is a proper way to call `get_face_detection_result(self, int image)` and `get_face_detection_image(self)` and `grab_face_detection_distance_image(self, depth)`:
```
ret, imgl = cam.grab_rgb(gs.FRAME_GRAB.LEFT)
ret, imgr = cam.grab_rgb(gs.FRAME_GRAB.RIGHT)
#grab face detect image
img_fd_depth = gs_facedetect.grab_face_detection_image(self)
#grab face detect image with distance
img_fd_depth = gs_facedetect.grab_face_detection_distance_image(imgl,imgr)
```
