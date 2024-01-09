# HAWK  Documents：Tutorials, API Refernce
## **Introduction**

The Hawk camera, engineered to emulate human visual perception, harnesses the power of its twin 'eyes' and triangulation techniques. This advanced approach enables the Hawk camera to generate a detailed three-dimensional insight into the viewed scene. This capability not only facilitates spatial awareness and motion detection for your applications but also enhances interactive experiences, making it ideal for applications in fields like AR(augmented reality), robotics, and advanced surveillance systems.
![HAWK](/resources/HAWK.jpg)
This guide will help you get started with the HAWK camera and HAWK SDK.
- Get started by reading the [Get Started](#get-started) part
- Learn more about the camera features of the HAWK camera
- Explore the applications, [Camera Control](#camera-control), [Depth Sensing](#depth-sensing), [Object Detection](#object-detection) and [Face Detection](#face-detection)

### Supported Platforms

Here is the list of all supported operating systems for the HAWK SDK .
-  JetPack 5.1.1 (L4T 35.3.1) 4.0.8 (Jetson Orin AGX)

### Integrations
  
The integration of the HAWK SDK into projects is straightforward and compatible with the following programming languages:
- **PYTHON**
---
## **Get Started**

Unpack your camera and Jetson developer kit, put the power on, connect the HAWK camera to the Jetson kit with the following cable options:<br>

1. 0.3M 4T1 cable (LI-FCB-4T1-SS-0.3M-NP-A0) + Fakra cable (FAK-SMZSMZ).
![Orin_Kit_HAWK](/resources/Orin_Kit_HAWK_1.png)

2. 2M 4T1 cable (LI-FCB-4T1-SS-2M-NP-T1).
![Orin_Kit_HAWK](/resources/Orin_Kit_HAWK_2.png)

The HAWK SDK is avialable for  NVIDIA® Jetson platform for now. We provide scripts to run the installation.
### Download and Install the SDK

To use the HAWK's cameras on NVIDIA® Jetson platforms, you need to:
- Setup JetPack
- Install the HAWK SDK for  NVIDIA® Jetson

#### Setup Jetpack
To use a NVIDIA® Jetson board, it is necessary to flash Jetpack, NVIDIA®'s proprietary system for Jetson. We recommend using NVIDIA® SDK Manager to flash the Jetpack **5.1.1** version. There is some steps and tips you should follow.

1. You can download the NVIDIA® [SDK Manager](https://developer.nvidia.com/sdk-manager) from the Jetpack SDK section on the  NVIDIA® website. While different operating system versions will correspond to different SDK versions Here is a supported OS table from the NVIDIA® website.
![Support_OS](/resources/Support_OS.png)

2. When you have downloaded the SDK manager from the official website, put it into the virtual machine operating system, let's take `ubuntu 20.04` as an example. Open a terminal in the current folder and execute two commands:
    ```
    sudo dpkg -i sdkmanager_2.0.0-11405_amd64.deb
    sdkmanager
    ```
    ![SDKManager_Installation](/resources/SDKManager_Installation.png)

3. Wait about 30s after entering the command, the NVIDIA® fllash interface will pop up, click LOGIN to login (please use your own account NVIDIA® to login). After login successfully, the interface will load automatically into STEP 01: select platform and version:System Configuration: Jetson AGX Orin modulesSDK Version: JetPack 5.1.1(rev.1),click CONTINUE.<br>
![Flash_step1](/resources/Flash_step1.png)<br>

4. Then, step 2. Check the "I agree" box and click CONTINUE. Jetson Linux and Jetson Runtime Components are checked by default. Make sure check the CUDA, it's a must for use the HAWK SDK. You can choose your own download path, we recommend using the default path.
![Flash_step2](/resources/Flash_step2.png)<br>

5. At this time, Orin will be powered on to reset the operation: Orin powered on, then connected to the computer, press the RECOVERY button on Orin and do not let go and then press the RESET button, and then release the RECOVERY button. Once Orin connect to the Virtual machine, At this time, a pop-up window will appear and enter STEP 03: Select hardware platform. Select the corresponding platform, click OK, and then you need to choose the way to flash. You can use a USB cable to connect Orin to your computer. In the pop-up window, select "Runtime" for the OEM Configuration option and "EMMC (default)" for the Storage Device option. Then, click "Flash" to enter the flashing mode.
![Flash_step3](/resources/Flash_step3.png)<br>
![Flash_step5](/resources/Flash_step5.png)<br>

6. When the system  start SDK flashing, waiting for the system to complete the flashing (SDK flashing takes a long time, need to wait a long time). After the flashing process is complete, you should start installing components. At this point, Orin will boot up and prompt you to configure the computer. Set up your username and password. Once inside Orin, locate your IP address. In the pop-up window of the SDK Manager, fill in the corresponding information, then click "install" to begin installing the components. <br>
![Flash_step4](/resources/Flash_step4.png)<br>
![Flash_step6](/resources/Flash_step6.png)<br>
6. When the inatallation is finished, it will go to STEP 04: just exit. Completion of flashing.
![Flash_step7](/resources/Flash_step7.png)<br>

#### Install the HAWK SDK for NVIDIA® Jetson
Please download the entire SDK repository. We provide Python scripts that can assist users in installing the camera drivers and using the SDK. The script file involves two parts: 1) driver installation, and 2) environment configuration setup. 
1. After downloading the GitHub repository , navigate to the repository directory, open the terminal in the current path and run 

    ```
    ./Installation_Script.sh
    ```

    When the following interface appears, it indicates that the installation is successful.
    ![Driver_Installation](/resources/Driver_Installation.png)

2. After downloading the GitHub repository , navigate to the repository directory, open the terminal in the current path and run 

    ```
    sudo chmod 777 Environment_Setup.sh
    ./Environment_Setup.sh
    ```

    When the following interface appears, it indicates that the installation is successful. Make sure you haven't encountered any red error messages. If you have, please rerun the process.
    ![Environment_Setup](/resources/Environment_Setup.png)
    > There is also a reminder for you to note: if you are in mainland China, you need to use a VPN before running this script. If you are not in mainland China, please ignore this reminder.
---
## **SDK Overview**

### Camera Control

The HAWK camera is equipped with ON Semiconductor 2.3MP CMOS digital image sensor AR0234CS, capable of producing clear, low noise images in both low-light and bright scenes. This stereo camera outputs 1920 ×1200 RAW data from each sensor.

There are several camera settings available for now. We offer the Full Resolution mode with an output resolution of 1920x1200 and a 30fps framerate. Additionally, you can capture photos, record videos, display camera information, and show Calibration information. Also, you can adjust exposure and gain in the Setting Menu.

Enter the application folder, then Preview folder. Open a terminal and run：
```
python3 main.py
```
![Camera_Control](/resources/Camera_Control.gif)
![CalibrationInformation](/resources/CalibrationInformation.png)
For more information on Camera Control, see the [API Reference](/APIReference.md) page.

### Depth Sensing 

The HAWK camera mimics the mechanism of human stereoscopic vision. Typically, the human eyes are spaced around 65 mm apart, providing each eye with a marginally different perspective of the surroundings. This variation in views allows the brain to discern depth and perceive three-dimensional motion. The camera analyzes the variations in pixel placement between the left and right images to calculate depth and track motion.

#### Depth Perception
Depth perception refers to the capacity to gauge the distance between various objects and visualize the environment in three dimensions. Historically, depth sensors have primarily been effective at short ranges and in indoor environments, which has confined their usage largely to applications like gesture recognition and body movement tracking. The depth sensor feature of HAWK camera:
- Depth can be captured at ranges up to 1m ~8m
- Frame rate of depth capture can be as high as 60 FPS
- Field of view(FOV) : 147.5°diagonal, 121.5°horizontal, 73.5°vertical

#### Depth Map
The HAWK camera creates depth maps by assigning a distance value (Z) to each pixel (X, Y) within the image. This distance, typically measured in metric units such as meters, represents the length from the rear of the camera's left eye to the object in the scene.

Depth maps are encoded in a 32-bit format, which means they cannot be directly visualized. For visual representation, it is essential to convert them into an 8-bit grayscale (monochrome) format, where the scale ranges from [0, 255]. In this scale, a value of 255 indicates the nearest depth measurement, while a value of 0 signifies the furthest possible depth measurement.

Enter the application folder, then Depth folder. Open a terminal and run：
```
python3 main.py
```
![Depth](/resources/Depth.gif)

For more information on Depth Sensing, see the [API Reference](/APIReference.md) page.

### Object Detection

Object detection involves recognizing and locating objects within an image. Leveraging depth sensing and 3D data, the HAWK camera is capable of determining both the 2D and 3D coordinates of objects present in the scene.
Utilizing artificial intelligence and neural networks, the HAWK SDK identifies objects in both left and right images. It then calculates the three-dimensional location of each object and their bounding boxes, employing information from its depth module. 

The HAWK SDK can detect all objects present in the images and recognize each object's identity. The object's distance from the camera is measured in metric units, such as meters, and is determined by calculating the length from the rear part of the camera's left eye to the object in the scene. Additionally, the SDK generates a 2D mask identifying the pixels in the left image that are part of the object. Using this, the HAWK camera is able to produce the 2D bounding boxes for these objects and, with the depth map's assistance, precisely calculate their 3D bounding boxes.

#### Detection Outputs
In the HAWK SDK, every detected object is represented as a structured entity that encompasses all pertinent information about the object. 

Enter the application folder, then `Objection detection` folder. Open a terminal and run：
```
python3 main.py
```
![Object_Detection.gif](/resources/Object_Detection.gif)

### Face Detection

Face detection finds and locates faces in images. The HAWK camera uses depth sensing and 3D data to determine both face coordinates. The SDK, powered by AI and neural networks, detects faces in left and right images. It then calculates face locations and bounding boxes, generating a 2D mask for faces in the left image. This allows the camera to produce 2D bounding boxes and accurately calculate 3D ones with the depth map's help.

#### Detection Outputs

Enter the application folder, then `Face detection` folder. Open a terminal and run：
```
python3 main.py
```
![Face_Detection.gif](/resources/Face_Detection.gif)

For more information on Face Detection, see the [API Reference](/APIReference.md) page.

---
### **Code Samples**

#### Samples

To make it easier for you to learn about spatial perception and AI, the HAWK SDK comes with a collection of helpful code examples. You can access all of these samples on HAWK's GitHub repository. Here is a code sample list for you to start with the HAWK.

| Sample | Description | Link |
| ---- | ---- | ---- |
| <br>Camera Control<br> | Previews and shows how came settings like Exposure, Gain, etc. can be modified  |[Camera Control](/APIReference.md#Camera)|
| Depth Sensing | Shows how to capture a Depth Map and Pseudo-color Map and display them in a window |[Depth Sensing](/APIReference.md#Camera)|
| Object Detection | Shows to recognize objects in the frame and generates a 2D bouncing box to distinguish between objects in the frame. | [Object Detection](/APIReference.md#Object-Detection) |
| Face Detection | Shows to recognize faces in the frame and generates a 2D bouncing box and keep faces in the frame.| [Face Detection](/APIReference.md#Face-Detection) |