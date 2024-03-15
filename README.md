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
- [Setup JetPack](#setup-jetpack) 
- [Install the HAWK SDK for  NVIDIA® Jetson](#install-the-hawk-sdk-for-nvidia®-jetson)

#### Setup Jetpack
To use a NVIDIA® Jetson board, it is necessary to flash Jetpack, NVIDIA®'s proprietary system for Jetson. We recommend using NVIDIA® SDK Manager to flash the Jetpack 5.1.1 version. This section will tells how to do, including:
- 	Preparing Hardware & Software
-	Flashing Jetson Linux System
-	Flashing CUDA

- **Preparing Hardware & Software**<br>
Before you start, make sure you have prepared the following hardware and software.
    |||
    |---|---|
    |Hardware|NVIDIA JETSON Orin Kit R35.3.1 x 1|
    |Software|Ubuntu 20.04|
    ||Python 3.8|
    ||CUDA Toolkit 11.4|
    ||TensorRT 8.4.1.5|
    ||Python setuptools 45.2.0+|
-  **Flashing Jetson Linux System**
1.	Download the NVIDIA® [SDK Manager](https://developer.nvidia.com/sdk-manager) from the Jetpack SDK section on the NVIDIA® website. 
While different operating system versions will correspond to different SDK versions. Here is a supported OS table from the NVIDIA® website.
![Support-OS](/resources/Support_OS.png)
2.	Copy the downloaded **sdkmanager_2.0.0-11405_amd64.deb** to the virtual machine.
3.	Run the following command in current folder.
```
# sudo dpkg -i sdkmanager_2.0.0-11405_amd64.deb
# sdkmanager
```
4.	Wait for about 20s. The Nvidia SDK Manager window pops up. Click **LOGIN**.
![SDKManager_Installation](/resources/SDKManager_Installation.png)
5.	Log in with your Nvidia account and password. 
6.	The STEP 01 DEVELOPMENT ENVIRONMENT window appears. Choose as the listed below and click **CONTINUE**.

    |||
    |---|---|
    |Product Category|Jetson|
    |System Configuration|	Host Machine|
    |Jetson |AGX Orin modules|
    |SDK Version| JetPack5.1.1 (rev.1)|

    ![Flash_step1](/resources/Flash_step1.png)

7.	While entering into STEP 02 DETAILS AND LICENSE, you have the following options.

    |**Options** |	**How to Configure**|
    |---|---|
    |Flash Jetson Linux	|Make sure the **Jetson Linux** checkbox is checked.<br> Default status: checked|
    |Flash CUDA|	Check the **Jetson Runtime Components** checkbox according to your needs. <br>Default status: checked<br> NOTE: If this checkbox is selected, CUDA flashing interface will be automatically displays after flashing Jetson Linux completes.|

    ![Flash_step2](/resources/Flash_step2.png)
8.	Set the download directory. It is recommended to use the default path. 
9.	Select **I accept the terms and conditions of the License agreements** and click **CONTINUE**.
    ![Flash_step3](/resources/Flash_step3.png)
10.	Reset the Orin as below steps.<br>
    a. Power on the Orin.<br>
    b.	Connect the Orin flashing port to the computer via flashing cable.<br>
    c.	Press and hold **RECOVERY** key on the Orin, then press **RESET** key.<br>
    d.	Release the **RECOVERY** key. The Orin will enter into flashing mode. <br>
    e.	If you want to check, run the following command.<br>
    
    ```
    #lsusb
    ```

    **NVIDIA Corp. APX** circled in red box in the following screenshot indicates the Orin has been successfully reset and connected to virtual machine.
    ![Flash_step4](/resources/Flash_step4.png)
    f.	For those who don’t do step e, please make sure your device has been successfully connected to virtual machine.
11.	After the Orin successfully reset, the following window pops up. Please select the Jetson AGX Orin you are using and click OK. The screenshot shown below is an example.
    ![Flash_step5](/resources/Flash_step5.png)
12.	Select as listed below and click **Flash**.

    |**Parameter**|	**How to Configure**|
    |---|---|
    |OEM Configuration|	Choose **Runtime** in the dropdown list.|
    |Storage Device|	Make sure its value is **EMMC (default)**.|

    ![Flash_step6](/resources/Flash_step6.png)
13.	The Orin starting flashing. It takes a long time. Wait patiently until the procedure finishes
    ![Flash_step7](/resources/Flash_step7.png)

- **Flashing CUDA**<br>
After successfully performing the steps in Flashing Jetson Linux System. The Orin will display a window.
1.	Set account and password and then enter the system.
2.	Connect a network cable to the Orin and check the IP address.
![Step 2 - Falshing CUDA](/resources/FalshingCUDA.png)
3.	The CUDA setting interface appears. Set as below.
    |**Parameter**	|**How to Configure**|
    |---|---|
    |Connection|	Choose Ethernet in the dropdown list.|
    |IP Address	|Set according to your actual environment.|
    |Username	|Input according to your actual settings in above Step 1.|
    |Password	|Input according to your actual settings in above Step 1.|

    The following screenshot is just an example.
    ![Flash_step8](/resources/Flash_step8.png)
4.	Click **Install**. 
5.	After the system successfully connects the Orin, it will start flashing CUDA to the Orin automatically. 
    ![Flash_step7](/resources/Flash_step7.png)
6.	Once the CUDA is completely flashed, the following interface STEP 04 SUMMARY FINALIZATION appears automatically. Click **FINISH**.
    ![Flash_step9](/resources/Flash_step9.png)

#### Install the HAWK SDK for NVIDIA® Jetson

Please download the entire SDK repository. We provide Python scripts that can assist users in installing the camera drivers and using the SDK. The script file involves two parts: 1) driver installation, and 2) environment configuration setup.
**Driver Installation**
1.	Download the GitHub repository.
2.	Navigate to the repository directory.
3.	Open the terminal in the current path and run the following script.
```
./Installation_Script.sh
```
When the following interface appears, it indicates that the installation is successful.
    ![Driver_Installation](/resources/Driver_Installation.png)

**Environment Configuration Setup**
1.	Download the GitHub repository.
2.	Navigate to the repository directory.
3.	Open the terminal in the current path and run the following script.
    > NOTE: 
For users in mainland China, please connect to VPN (Virtual Private Network) before running the script.
```
sudo chmod 777 Environment_Setup.sh
./Environment_Setup.sh
```
When the following interface appears, it indicates that the installation is successful. Make sure you haven't encountered any red error messages. If you have, please rerun the process.
![Environment_Setup](/resources/Environment_Setup.png)

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