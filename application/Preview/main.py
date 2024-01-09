import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../../')
import PyGs.gs as gs
from ui.MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QLabel, QWidget
from PyQt5.QtCore import QTimer, QDateTime, Qt, QDate, QStandardPaths
import cv2
from PyQt5.QtGui import QPixmap, QImage
import time
import os
from application.Preview.ui.Setting import Ui_Form

folder_path_global = 0

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.camera = gs.Camera()
        self.camera_info = gs.CameraInformation()
        self.init_camera()
        self.button_original_style = self.ui.pushButton_7.styleSheet()
        self.ui.pushButton_7.clicked.connect(self.start_stop_recording)
        self.ui.pushButton_6.clicked.connect(self.take_photo)
        self.ui.pushButton_3.clicked.connect(self.select_save_directory)
        self.ui.comboBox.currentIndexChanged.connect(self.change_resolution)
        self.ui.comboBox_4.currentIndexChanged.connect(self.change_framerate)
        self.start_time = time.time()
        self.recording = False
        self.video_writer = None
        self.filename = None
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.photo_count = 0
        self.ui.pushButton_20.clicked.connect(self.on_pushButton_20_clicked)
        self.settings_window = SettingsWindow(self.camera, self)
        serial_number = self.camera_info.serial_number
        self.ui.label.setText(serial_number)
        self.init_info_labels()  # Calls the initialization information label method

    def closeEvent(self, event):
        # Close the Settings page
        if hasattr(self, 'settings_window') and self.settings_window is not None:
            self.settings_window.close()

        # Increase the delay and wait for the resource release
        QtCore.QCoreApplication.processEvents()
        time.sleep(1)

        # Turn off the camera
        self.camera.close()

        # Invoke the close event handling of the parent class
        super().closeEvent(event)

    def on_pushButton_20_clicked(self):
        # Show Settings window
        self.settings_window.show()

    def init_camera(self):
        init_params = gs.InitParameters()
        init_params.camera_id = 0
        init_params.camera_ae = 1
        ret = self.camera.open(init_params)


        if ret == gs.ERROR_CODE.ERROR:
            print("Failed to open the camera.")
            QMessageBox.critical(self, "Error", "Failed to open the camera.")
            self.close()

        resolutions = [(1920, 1200)]
        for resolution in resolutions:
            self.ui.comboBox.addItem(f"{resolution[0]}x{resolution[1]}")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_info_labels(self):
        self.labelModelInfo = self.ui.Model
        self.labelResolutionInfo = self.ui.Resolution
        self.labelFramerateInfo = self.ui.Framerate
        self.labelFrameDropInfo = self.ui.Frame_Drop

    def update_frame(self):
        ret_left, frame_left = self.camera.grab_rgb(gs.FRAME_GRAB.LEFT)
        ret_right, frame_right = self.camera.grab_rgb(gs.FRAME_GRAB.RIGHT)

        if ret_left and ret_right:
            # Process left camera images
            rgb_image_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)
            h_left, w_left, ch_left = rgb_image_left.shape
            bytes_per_line_left = ch_left * w_left
            qimg_left = QImage(rgb_image_left.data, w_left, h_left, bytes_per_line_left, QImage.Format_RGB888)

            # Resize the image and set to QLabel
            qimg_left = qimg_left.scaled(self.ui.LeftWindow.size(), Qt.KeepAspectRatio)
            self.ui.LeftWindow.setPixmap(QPixmap.fromImage(qimg_left))

            # Process right camera images
            rgb_image_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
            h_right, w_right, ch_right = rgb_image_right.shape
            bytes_per_line_right = ch_right * w_right
            qimg_right = QImage(rgb_image_right.data, w_right, h_right, bytes_per_line_right, QImage.Format_RGB888)

            # Resize the image and set to QLabel
            qimg_right = qimg_right.scaled(self.ui.RightWindow.size(), Qt.KeepAspectRatio)
            self.ui.RightWindow.setPixmap(QPixmap.fromImage(qimg_right))

            if self.recording and self.video_writer is not None:
                self.record_frame(frame_right)

        # Update information tag
        self.update_info_labels()

    def update_info_labels(self):
        camera_info = self.camera.get_camera_information()  # Get camera information
        left_resolution = (int(self.camera.cam_L.get(cv2.CAP_PROP_FRAME_WIDTH)),
                           int(self.camera.cam_L.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        right_resolution = (int(self.camera.cam_R.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            int(self.camera.cam_R.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # Get left and right camera resolution

        camera_model = camera_info.camera_model  # Get camera model
        framerate = int(self.camera.cam_L.get(cv2.CAP_PROP_FPS))
        running_time_info = self.get_running_time()  # Get camera duration
        current_date_time = QDateTime.currentDateTime()
        current_date = current_date_time.toString("yyyy-MM-dd hh:mm:ss")

        # Gets the current day of the week
        day_of_week = QDate(current_date_time.date()).toString("dddd")

        # Displays the Date, time, and day of the week on the Date button
        date_text = f"Date: {current_date}"
        self.ui.Date.setText(date_text)

        self.labelModelInfo.setText(f"Model: {camera_model}")
        self.labelResolutionInfo.setText(f"Left Resolution: {left_resolution[0]}x{left_resolution[1]}, "
                                         f"Right Resolution: {right_resolution[0]}x{right_resolution[1]}")
        self.labelFramerateInfo.setText(f"Framerate: {framerate} FPS")
        self.labelFrameDropInfo.setText(f"Runing Time: {running_time_info}")

    def get_running_time(self):
        elapsed_time = time.time() - self.start_time
        return f"{int(elapsed_time)} seconds"

    def change_resolution(self):
        resolution_str = self.ui.comboBox.currentText()
        width, height = map(int, resolution_str.split("x"))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        index = self.ui.comboBox.currentIndex()
        self.ui.comboBox.setItemText(index, f"{width}x{height}")
        print("change_resolution called")

        # Update information tag
        self.update_info_labels()

    def change_framerate(self):
        print("change_framerate called")
        framerate = int(self.ui.comboBox_4.currentText())
        self.camera.set(cv2.CAP_PROP_FPS, framerate)

        # Update information tag
        self.update_info_labels()

    def save_photo(self, frame):
        # The default path is /home/Pictures
        default_directory = os.path.join(QStandardPaths.writableLocation(QStandardPaths.HomeLocation), "Pictures")
        if folder_path_global != 0:
            default_directory = folder_path_global
        # Construct default file name
        self.photo_count += 1
        default_photo_path = os.path.join(default_directory, f"photo_{self.photo_count}.png")

        # Save photo directly
        cv2.imwrite(default_photo_path, frame)

        # If necessary, the current save path is displayed on the screen
        if hasattr(self.ui, 'label_7') and isinstance(self.ui.label_7, QLabel):
            self.ui.label_7.setText(f"Current Path: {default_directory}")

    def take_photo(self):
        ret_right, frame_right = self.camera.grab_rgb(gs.FRAME_GRAB.RIGHT)
        if ret_right:
            self.save_photo(frame_right)

    def select_save_directory(self):
        # Open the folder selection dialog box
        global folder_path_global
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path_global = QFileDialog.getExistingDirectory(self, "Select the folder to save the picture", "", options=options)

        if folder_path_global:
           QMessageBox.information(self, "Save picture", folder_path_global)
        else:
            QMessageBox.warning(self, "Save picture", "No save folder was selected.")

    def record_frame(self, frame):
        if self.video_writer is None:
            self.filename = f"recording_{int(time.time())}.avi"
            pictures_location = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            full_path = os.path.join(pictures_location, self.filename)
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(full_path, self.fourcc, 30.0, (1920, 1200))


        self.video_writer.write(frame)

    def start_stop_recording(self):
        self.recording = not self.recording

        if self.recording:
            self.ui.pushButton_7.setStyleSheet("background-color: red;")
            self.filename = f"recording_{int(time.time())}.avi"
            videos_location = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
            self.full_path = os.path.join(videos_location, self.filename)
            self.video_writer = cv2.VideoWriter(self.full_path, self.fourcc, 30.0, (1920, 1200))


        else:
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
                self.ui.pushButton_7.setStyleSheet(self.button_original_style)
                print(f"Video writer released for {self.full_path}")


class SettingsWindow(QWidget, Ui_Form):
    def __init__(self, camera, main_window):
        super().__init__()
        self.setupUi(self)

        self.cam = camera
        self.main_window = main_window  # Pass the main window instance
        self.setFixedSize(self.size())

        self.camera_info = gs.CameraInformation()
        self.camera_info.get_calibration_data()
        self.label_612.setText(str(float(self.camera_info.mtxL_fx)))
        self.label_7.setText(str(float(self.camera_info.mtxL_fy)))
        self.label_8.setText(str(float(self.camera_info.mtxL_cx)))
        self.label_9.setText(str(float(self.camera_info.mtxL_cy)))
        self.label_10.setText(str(float(self.camera_info.mtxL_k1)))
        self.label_11.setText(str(float(self.camera_info.mtxL_k2)))
        self.label_12.setText(str(float(self.camera_info.mtxL_p1)))
        self.label_13.setText(str(float(self.camera_info.mtxL_p2)))
        self.label_14.setText(str(float(self.camera_info.mtxL_k3)))
        self.label_17.setText(str(float(self.camera_info.mtxR_fx)))
        self.label_21.setText(str(float(self.camera_info.mtxR_fy)))
        self.label_22.setText(str(float(self.camera_info.mtxR_cx)))
        self.label_24.setText(str(float(self.camera_info.mtxR_cy)))
        self.label_26.setText(str(float(self.camera_info.mtxR_k1)))
        self.label_43.setText(str(float(self.camera_info.mtxR_k2)))
        self.label_44.setText(str(float(self.camera_info.mtxR_p1)))
        self.label_45.setText(str(float(self.camera_info.mtxR_p2)))
        self.label_46.setText(str(float(self.camera_info.mtxR_k3)))
        self.groupBox_3.setVisible(False)
        
        # Connect slot functions for four buttons that jump to different pages
        self.push1.clicked.connect(self.show_page)
        self.push2.clicked.connect(self.show_page_2)
        self.push3.clicked.connect(self.show_page_3)
        self.push4.clicked.connect(self.show_page_4)
        self.defa_1.clicked.connect(self.reset_default_values)
        self.pushButton_5.clicked.connect(self.select_save_directory)  # Connect button click the event to select the method to save the folder

        # The first page is displayed
        self.General_2.setCurrentIndex(0)

        # Gets and displays the values for the initial four Settings
        self.display_initial_settings(gs.VIDEO_SETTINGS.BRIGHTNESS, self.slide_1, self.lab1)
        self.display_initial_settings(gs.VIDEO_SETTINGS.CONTRAST, self.slide_2, self.lab2)
        self.display_initial_settings(gs.VIDEO_SETTINGS.GAIN, self.slide_3, self.lab3)
        self.display_initial_settings(gs.VIDEO_SETTINGS.EXPOSURE, self.slide_4, self.lab4)

        # Connect the signal slot for the slider value change
        self.slide_1.valueChanged.connect(
            lambda value: self.update_camera_settings(value, gs.VIDEO_SETTINGS.BRIGHTNESS, self.lab1))
        self.slide_2.valueChanged.connect(
            lambda value: self.update_camera_settings(value, gs.VIDEO_SETTINGS.CONTRAST, self.lab2))
        self.slide_3.valueChanged.connect(
            lambda value: self.update_camera_settings(value, gs.VIDEO_SETTINGS.GAIN, self.lab3))
        self.slide_4.valueChanged.connect(
            lambda value: self.update_camera_settings(value, gs.VIDEO_SETTINGS.EXPOSURE, self.lab4))

        # Example Initialize the default value
        self.default_brightness = self.cam.get_camera_settings(gs.VIDEO_SETTINGS.BRIGHTNESS)
        self.default_contrast = self.cam.get_camera_settings(gs.VIDEO_SETTINGS.CONTRAST)
        self.default_gain = 3
        self.default_exposure = 130

    def display_initial_settings(self, setting_type, slider, label):
        current_value = self.cam.get_camera_settings(setting_type)
        current_value = int(current_value / 100)  # Convert a floating point number to an integer
        slider.setValue(current_value)
        label.setText(f"{setting_type}: {current_value}")

    def update_camera_settings(self, value, setting_type, label):
        value = value * 100
        self.cam.set_camera_video_settings(setting_type, value)
        current_value = self.cam.get_camera_settings(setting_type)
        current_value = current_value / 100
        label.setText(f"{setting_type}: {current_value}")

    def show_page(self):
        self.General_2.setCurrentIndex(0)
        self.repaint()

    def show_page_2(self):
        self.General_2.setCurrentIndex(1)
        self.repaint()

    def show_page_3(self):
        self.General_2.setCurrentIndex(2)

    def show_page_4(self):
        self.General_2.setCurrentIndex(3)

    def on_push1_clicked(self):
        self.page.hide()
        self.page_2.show()
        self.page_3.hide()
        self.page_4.hide()

    # The new method is used to restore the camera Settings to default values
    def reset_default_values(self):
        # Restore to default brightness, contrast, gain, and exposure values
        self.set_default_values(self.default_brightness, gs.VIDEO_SETTINGS.BRIGHTNESS, self.slide_1, self.lab1)
        self.set_default_values(self.default_contrast, gs.VIDEO_SETTINGS.CONTRAST, self.slide_2, self.lab2)
        self.set_default_values(self.default_gain, gs.VIDEO_SETTINGS.GAIN, self.slide_3, self.lab3)
        self.set_default_values(self.default_exposure, gs.VIDEO_SETTINGS.EXPOSURE, self.slide_4, self.lab4)

    # The new method is used to set camera parameters to specified values
    def set_default_values(self, default_value, setting_type, slider, label):
        # Set the value of the slider and update the text of the label

        self.update_camera_settings(default_value, setting_type, label)
        slider.setValue(default_value)

    # Added a method for selecting a folder to save
    def select_save_directory(self):
        global folder_path_global
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path_global = QFileDialog.getExistingDirectory(self, "Select the folder to save the picture", "", options=options)

        if folder_path_global:
            QMessageBox.information(self, "Save picture", folder_path_global)
            # Call the main window method here to update the save folder path
            self.main_window.ui.label_7.setText(f"Current Path: {folder_path_global}")
            # Update label_74
            self.label_74.setText(f"Current Path: {folder_path_global}")
        else:
            # If no save folder is selected, the default path is displayed
            default_directory = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            QMessageBox.warning(self, "Save picture", "No save folder was selected.")
            # Update label_74
            self.label_74.setText(f"Current Path: {default_directory}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
