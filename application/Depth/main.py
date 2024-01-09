import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../../')
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from ui.Mainwindow import Ui_MainWindow
import PyGs.gs as gs
import qimage2ndarray


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # set ui
        self.camera = gs.Camera()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # initialize the camera
        init_params = gs.InitParameters()
        init_params.camera_id = 0  # Set the camera ID and adjust it according to your Settings
        init_params.camera_width = gs.RESOLUTION.FULL_RES[0]
        init_params.camera_height = gs.RESOLUTION.FULL_RES[1]
        init_params.camera_resolution = gs.RESOLUTION.HD1080P  # Set camera resolution
        init_params.camera_fps = gs.FRAME_RATE.FPS_30  # Set frame rate
        self.camera.open(init_params)
       # self.ui.depthModeChangedSignal.connect(self.change_depth_mode)

        # create QTimer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # set depth mode
        if self.camera.set_depth_mode(gs.DEPTH_MODE.TENSORT) == gs.ERROR_CODE.ERROR:
            print("set_depth_mode Failed")
            exit(0)
    def depth_data_to_qimage(self, depth_data):
        # The depth data is normalized
        depth_normalized = (
                    (depth_data - np.min(depth_data)) * (1 / (np.max(depth_data) - np.min(depth_data)) * 255)).astype(
            np.uint8)
        h, w = depth_normalized.shape
        # Create the QImage object
        return QImage(depth_normalized.data, w, h, w, QImage.Format_Grayscale8)

    def update_frame(self):
        camera_fps = self.camera.camera_fps
        self.ui.label_2.setText(f"FPS: Camera: {camera_fps}Hz | Depth: {camera_fps}Hz")
        index = self.ui.comboBox.currentIndex()
        ret, img = self.camera.grab_rgb(index)
        if ret:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(image)
            # Create QPixmap and scale to QLabel size
            pixmap = QPixmap(qimg)
            scaled_pixmap = pixmap.scaled(self.ui.original_output.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

            # Set the scaled image to QLabel
            self.ui.original_output.setPixmap(scaled_pixmap)
            self.ui.original_output.show()


         # Depth mode
        depth_data = self.camera.grab_depth_data()
        if depth_data is not None:
            disparity_data = self.camera.grab_disparity()
            depth_data_disp = self.depth_data_to_qimage(disparity_data)
            pixmap = QPixmap.fromImage(depth_data_disp)
            self.ui.depthsensing_output.setPixmap(pixmap.scaled(self.ui.depthsensing_output.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))

            pseudo_data = self.camera.grab_depth_pseudo()
            image = cv2.cvtColor(pseudo_data, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(image)
            # Create QPixmap and scale to QLabel size
            pseudo_pixmap = QPixmap(qimg)
            self.ui.pseudo_output.setPixmap(pseudo_pixmap.scaled(self.ui.pseudo_output.size(), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))


def closeEvent(self, event):
    # Stop video capture when the window closes
    self.capture.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    camera = gs.Camera()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
