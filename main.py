# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
import time
from PySide6.QtCore import QThread


class StopWatch(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.h = 0
        self.m = 0
        self.s = 0

    def reset(self):
        self.h = 0
        self.m = 0
        self.s = 0

    def increase(self):
        self.s += 1
        if self.s >= 60:
            self.s = 0
            self.m += 1
        if self.m >= 60:
            self.m = 0
            self.h += 1

    def run(self):
        while True:
            self.increase()
            window.ui.lbl_stopwatch.setText(f"{'%0.2d' % self.h}:{'%0.2d' % self.m}:{'%0.2d' % self.s}")
            time.sleep(1)

class Timerr(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.h = window.ui.sp_h.value()
        self.m = window.ui.sp_m.value()
        self.s = window.ui.sp_s.value()

    def reset(self):
        self.h = 0
        self.m = 0
        self.s = 0

    def decrease(self):
        if self.s == 0 and self.m == 0 and self.h == 0:
            return
        if self.s <= 0:
            self.m -= 1
            self.s += 60
        if self.m < 0:
            self.h -= 1
            self.m += 60
        self.ss -= 1

    def run(self):
        while True:
            self.decrease()
            window.ui.lbl_timer.setText(f"{'%0.2d' % self.h}:{'%0.2d' % self.m}:{'%0.2d' % self.s}")
            time.sleep(1)


class Timer(QWidget):
    def __init__(self):
        super(Timer, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        # stopwatch
        self.ui.btn_stopwatch_start.clicked.connect(self.start_stopwatch)
        self.ui.btn_stopwatch_pause.clicked.connect(self.pause_stopwatch)
        self.ui.btn_stopwatch_stop.clicked.connect(self.stop_stopwatch)
        self.ui.btn_stopwatch_save.clicked.connect(self.save_stopwatch)
        # timer
        self.ui.btn_timer_start.clicked.connect(self.start_timer)
        self.ui.btn_timer_pause.clicked.connect(self.pause_timer)
        self.ui.btn_timer_stop.clicked.connect(self.stop_timer)
        self.stopwatch = StopWatch()
        self.timer = Timerr()
        self.ui.show()

    def start_stopwatch(self):
        self.stopwatch.start()

    def pause_stopwatch(self):
        self.stopwatch.terminate()

    def stop_stopwatch(self):
        self.stopwatch.terminate()
        self.stopwatch.reset()
        self.ui.lbl_stopwatch.setText('00:00:00')

    def save_stopwatch(self):
        label = QLabel()
        label.setStyleSheet('font: 16pt "Comic Sans MS"; color: rgb(55, 17, 135);')
        label.setText(self.ui.lbl_stopwatch.text())
        self.ui.vl.addWidget(label)

    def start_timer(self):
        self.timer.start()

    def pause_timer(self):
        self.timer.terminate()

    def stop_timer(self):
        self.timer.terminate()
        self.ui.lbl_timer.setText("00:00:00")
        self.timer.reset()


if __name__ == "__main__":
    app = QApplication([])
    window = Timer()
    sys.exit(app.exec())
