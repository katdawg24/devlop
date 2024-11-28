# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

import SerialWorker
import TempDialog
import DistanceDialog
import pandas as pd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1108, 798)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.depth_display = QtWidgets.QLCDNumber(self.centralwidget)
        self.depth_display.setGeometry(QtCore.QRect(730, 70, 201, 61))
        self.depth_display.setObjectName("depth_display")
        self.temp_display = QtWidgets.QLCDNumber(self.centralwidget)
        self.temp_display.setGeometry(QtCore.QRect(190, 70, 201, 61))
        self.temp_display.setObjectName("temp_display")


        self.motor_speed_slider = QtWidgets.QSlider(self.centralwidget)
        self.motor_speed_slider.setGeometry(QtCore.QRect(260, 610, 611, 31))
        self.motor_speed_slider.setOrientation(QtCore.Qt.Horizontal)
        self.motor_speed_slider.setObjectName("motor_speed_slider")
        self.motor_speed_slider.valueChanged.connect(self.update_motor_speed)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(490, 560, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 20, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(790, 20, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.temp_menu_button = QtWidgets.QPushButton(self.centralwidget)
        self.temp_menu_button.setGeometry(QtCore.QRect(170, 420, 231, 51))
        self.temp_menu_button.setObjectName("temp_menu_button")
        self.temp_menu_button.clicked.connect(self.openTempMenu)

        self.distance_menu_button = QtWidgets.QPushButton(self.centralwidget)
        self.distance_menu_button.setGeometry(QtCore.QRect(710, 420, 231, 51))
        self.distance_menu_button.setObjectName("distance_menu_button")
        self.distance_menu_button.clicked.connect(self.openDistanceMenu)

        self.motor_menu_button = QtWidgets.QPushButton(self.centralwidget)
        self.motor_menu_button.setGeometry(QtCore.QRect(450, 660, 241, 51))
        self.motor_menu_button.setObjectName("motor_menu_button")

        

        self.small_temp_chart = pg.PlotWidget(self.centralwidget)
        self.small_temp_chart.setBackground("w")
        pen = pg.mkPen(color=(255,0,0))
        self.small_temp_chart.setTitle("Temperature vs Time", color="k", size="15pt")
        styles = {"color": "red", "font-size": "10px"}
        self.small_temp_chart.setLabel("left", "Temperature (°C)", **styles)
        self.small_temp_chart.setLabel("bottom", "Time (min)", **styles)
        #self.small_temp_chart.addLegend()
        self.small_temp_chart.showGrid(x=True, y=True)
        self.small_temp_chart.setYRange(17, 28)
        # self.time = list(range(10))
        # self.temperature = [30 + ((randint(1, 19) - 10) * 0.1) for _ in range(10)]

        self.time = []
        self.temperature = []

        self.temp_line = self.small_temp_chart.plot(
            self.time,
            self.temperature,
            name="Temperature Sensor",
            pen=pen
        )

        self.small_temp_chart.setGeometry(QtCore.QRect(60, 160, 461, 241))
        self.small_temp_chart.setObjectName("small_temp_chart")

        self.small_depth_chart = pg.PlotWidget(self.centralwidget)
        self.small_depth_chart.setBackground("w")
        pen = pg.mkPen(color=(255,0,0))
        self.small_depth_chart.setTitle("Depth vs Time", color="k", size="15pt")
        styles = {"color": "red", "font-size": "10px"}
        self.small_depth_chart.setLabel("left", "Distance (units)", **styles)
        self.small_depth_chart.setLabel("bottom", "Time (min)", **styles)
        #self.small_depth_chart.addLegend()
        self.small_depth_chart.showGrid(x=True, y=True)
        self.small_depth_chart.setYRange(325, 425)
        
        #self.distance = [60 + ((randint(1, 19) - 10) * 0.1) for _ in range(10)]
        self.distance = []

        self.depth_line = self.small_depth_chart.plot(
            self.time,
            self.distance,
            name="Lidar Sensor",
            pen=pen
        )
        self.small_depth_chart.setGeometry(QtCore.QRect(590, 160, 461, 241))
        self.small_depth_chart.setObjectName("small_depth_chart")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1108, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.df = pd.DataFrame(columns= ["Time", "Temp", "Distance"])
        self.serial_thread = SerialWorker.SerialWorker('COM3', 9600)  # Replace with your port and baudrate
        self.serial_thread.data_received.connect(self.update_plot)
        self.serial_thread.start()

        self.temp_window = None
        self.distance_window = None

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):  
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Motor Speed"))
        self.label_2.setText(_translate("MainWindow", "Temperature"))
        self.label_3.setText(_translate("MainWindow", "Depth"))
        self.temp_menu_button.setText(_translate("MainWindow", "Temperature Details"))
        self.distance_menu_button.setText(_translate("MainWindow", "Distance Details"))
        self.motor_menu_button.setText(_translate("MainWindow", "Manage Motor"))

    def update_plot(self, data):
        #Move least recent reading off graph
        if (len(self.time) > 19):
            self.time = self.time[1:]
            self.temperature = self.temperature[1:]
            self.distance = self.distance[1:]

        self.df.loc[len(self.df)] = [float(data[0]), float(data[1]), float(data[2])]

        self.time.append(float(data[0]))
        self.temperature.append(float(data[1]))
        self.distance.append(float(data[2]))

        #Redraw line
        self.temp_line.setData(self.time, self.temperature)
        self.depth_line.setData(self.time, self.distance)

        self.temp_display.display(self.temperature[-1])
        self.depth_display.display(self.distance[-1])

        if self.temp_window:
            
            self.temp_window.update_chart_data(data)

        if self.distance_window:
            
            self.distance_window.update_chart_data(data)

    def update_motor_speed(self, value):
        # Send motor speed value to Arduino
        if self.serial_thread:
            speed_data = f"SPEED {value}\n"
            self.serial_thread.send_data(speed_data)  # Send data via SerialWorker

    def openTempMenu(self):
        
            self.temp_window = TempDialog.Ui_TempDetails(self.df)
            self.serial_thread.data_received.connect(self.temp_window.update_chart_data)
            self.serial_thread.data_received.connect(self.temp_window.update_table)

        
    def openDistanceMenu(self):
        
            self.distance_window = DistanceDialog.Ui_DistanceDetails(self.df)
            self.serial_thread.data_received.connect(self.distance_window.update_chart_data)
            self.serial_thread.data_received.connect(self.distance_window.update_table)

    def closeEvent(self, event):
        self.serial_thread.stop()
        event.accept()
        

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
