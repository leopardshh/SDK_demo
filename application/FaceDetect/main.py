from Fcaedetect import Ui_Fcaedetect
import sys, os
sys.path.insert(0, '..')
sys.path.insert(0, '../../')
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QLabel,QSizePolicy,QMessageBox,QVBoxLayout, QDialog,QTextEdit,QScrollBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPainter
from io import StringIO
from PyQt5 import QtCore
import time
import cv2
import qimage2ndarray
import numpy as np
from datetime import datetime
import PyGs.gs as gs


class PrintDialog():
    def __init__(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('Face Detection')
        self.dialog.setGeometry(800, 800, 800, 800)

        # Create a label called result and use it to display printed_info in real time
        self.result_textedit = QTextEdit(self.dialog)
        self.result_textedit.setReadOnly(True)  # Set to read-only
        self.result_textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.layout = QVBoxLayout(self.dialog)
        self.layout.addWidget(self.result_textedit)
        self.printed_info = ""
        
    def showMessage(self, message):
        if message != ():
            self.printed_info = str(message)
        self.result_textedit.append(self.printed_info)

class Ui_Fcaedetect(QMainWindow,Ui_Fcaedetect):
    printSignal = QtCore.pyqtSignal(object)
    def __init__(self,parent=None):
        super(Ui_Fcaedetect,self).__init__(parent)
        self.setupUi(self)
        self.Callback()
        self.update_camera_info()
        
        self.mesDialog = PrintDialog()
        
        self.printSignal.connect(self.mesDialog.showMessage)
        
        
    def Callback(self):
        #self.comboBox.currentIndexChanged.connect(self.on_comboBox1_changed)
        self.exit_Pb.clicked.connect(self.exit_camera)
        #self.pushButton.setToolTip('exit app')
        self.save_image_Pb.clicked.connect(self.saveImage)
        self.result_Pb.clicked.connect(self.showDialog)
        
        # initialize the camera
        self.camera = gs.Camera()
        init_params = gs.InitParameters()
        init_params.camera_id = 0
        ret=self.camera.open(init_params)
        if ret == gs.ERROR_CODE.ERROR:
            print("open device Failed")
            exit(0)     

        
        # Create a timer to update the camera feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.timeout.connect(self.update_camera_info)
        #self.timer.timeout.connect(self.showDialog)
        self.timer.start(30)
        
        #if self.camera.set_depth_mode(gs.DEPTH_MODE.VPI) == gs.ERROR_CODE.ERROR:
        #    print("set_depth_mode Failed")
        #    exit(0)
        #self.gs_objdetect = gs.ObjectDetection()
        # enable
        #self.gs_objdetect.enable_object_detection(True)
        # start
        #self.gs_objdetect.object_detection()

        #face detect
        self.faceDetect = gs.FaceDetection()
        # enable
        self.faceDetect.enable_face_detection(True)

    def update_camera_info(self):
        # Get camera information
        camera_info = self.camera.get_camera_information()
        serial_number = camera_info.serial_number
        camera_model = camera_info.camera_model
        camera_id = camera_info.camera_id
        self.cam_serial_Lb.setText(f"serial_number: {serial_number}")
        self.cam_serial_Lb.setStyleSheet("color: black")
        self.cam_module_Lb.setText(f"camera_model: {camera_model}")
        self.cam_module_Lb.setStyleSheet("color: black")
        self.cam_id_Lb.setText(f"camera_id: {camera_id}")
        self.cam_id_Lb.setStyleSheet("color: black")

    def update_current_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_Pb.setText(f"Date: {current_time}")
        self.time_Pb.setStyleSheet("color: black")

    def update_frame(self):
        # Original video
        ret, imgL = self.camera.grab_rgb(gs.FRAME_GRAB.LEFT)
        imgL = cv2.resize(imgL, (640, 480))
        self.face_res = self.faceDetect.get_face_detection_result(imgL)
        if self.face_res != ():
            self.printSignal.emit(self.face_res)
        self.disp_objdetect = self.faceDetect.grab_face_detection_image()
        disp_objdetect_ = cv2.resize(self.disp_objdetect,(640,480))
        if ret:
            # transfer color zone into RGB
            int8_image = cv2.convertScaleAbs(disp_objdetect_)
            image = cv2.cvtColor(int8_image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            step = channel * width
            qimg = qimage2ndarray.array2qimage(image)
            self.label.setPixmap(QPixmap(qimg))
            self.label.show()
            
    def saveImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (.png .jpg *.jpeg)", options=options)
        if file_name and self.disp_objdetect is not None:
            cv2.imwrite(file_name, self.disp_objdetect)

    def showDialog(self):
        #self.mesDialog.exec_()
        self.mesDialog.dialog.show()

    
    def exit_camera(self):
        # Stop the camera and close the application
        self.close()
           
if __name__ == '__main__':
    app = QApplication(sys.argv)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    ui=Ui_Fcaedetect()
    ui.show()
    sys.exit(app.exec_())
