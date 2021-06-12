# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
import time
from PySide6.QtCore import QThread,Signal
from datetime import datetime
from playsound import playsound



class StopWatch(QThread):
    stp_run_signal=Signal()
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
            self.stp_run_signal.emit()
            time.sleep(1)

class Timerr(QThread):
    timer_setValue_signal=Signal()
    timer_ResetValue_signal = Signal()
    timer_run_signal=Signal()
    def __init__(self):
        QThread.__init__(self)
        self.h = 0
        self.m = 0
        self.s = 0

    def reset(self):
        self.h = 0
        self.m = 0
        self.s = 0
        self.timer_ResetValue_signal.emit()

    def set(self):
        self.timer_setValue_signal.emit()


    def decrease(self):
        if self.s == 0 and self.m == 0 and self.h == 0:
            return
        if self.s <= 0:
            self.m -= 1
            self.s += 60
        if self.m < 0:
            self.h -= 1
            self.m += 60
        self.s -= 1

    def run(self):
        self.set()
        while True:
            self.decrease()
            self.timer_run_signal.emit()
            time.sleep(1)

class Alarm(QThread):
    enable_alarm_signal = Signal()
    def __init__(self):
        QThread.__init__(self)
        self.h = 0
        self.m = 0
        self.s = 0

    def reset(self):
        self.h = 0
        self.m = 0

    def run(self):
        self.enable_alarm_signal.emit()
        while True:
            self.hour = int(datetime.now().strftime("%H"))
            self.minute = int(datetime.now().strftime("%M"))
            if self.hour == self.h and self.minute == self.m :
                    playsound('sound.WAV')
                    break


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
        #Alarm
        self.ui.btn_alarm_on.clicked.connect(self.enable_alarm)
        self.ui.btn_alarm_off.clicked.connect(self.disable_alarm)
        self.ui.btn_alarm_off.hide()
        self.stopwatch = StopWatch()
        self.timer = Timerr()
        self.alarm=Alarm()
        self.ui.show()

    def start_stopwatch(self):
        self.stopwatch.start()
        self.stopwatch.stp_run_signal.connect(self.update_stopwatch)
    def update_stopwatch(self):
        self.ui.lbl_stopwatch.setText(f"{'%0.2d' % self.stopwatch.h}:{'%0.2d' % self.stopwatch.m}:{'%0.2d' % self.stopwatch.s}")
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

    def setValueTimer(self):
        self.timer.h = self.ui.sp_h.value()
        self.timer.m= self.ui.sp_m.value()
        self.timer.s = self.ui.sp_s.value()

    def resetValueTimer(self):
        self.ui.sp_h.setValue(0)
        self.ui.sp_m.setValue(0)
        self.ui.sp_s.setValue(0)

    def start_timer(self):
        self.timer.start()
        self.timer.timer_setValue_signal.connect(self.setValueTimer)
        self.timer.timer_run_signal.connect(self.update_timer)

    def update_timer(self):
        self.ui.lbl_timer.setText(f"{'%0.2d' % self.timer.h}:{'%0.2d' % self.timer.m}:{'%0.2d' % self.timer.s}")

    def pause_timer(self):
        window.ui.sp_h.setValue(self.timer.h)
        window.ui.sp_m.setValue(self.timer.m)
        window.ui.sp_s.setValue(self.timer.s)
        self.timer.terminate()


    def stop_timer(self):
        self.timer.terminate()
        self.timer.timer_ResetValue_signal.connect(self.resetValueTimer)
        self.ui.lbl_timer.setText("00:00:00")
        self.timer.reset()


    def enable_alarm(self):
        self.alarm.start()
        self.alarm.enable_alarm_signal.connect(self.setAlarm)
        self.ui.btn_alarm_on.hide()
        self.ui.btn_alarm_off.show()

    def setAlarm(self):
        self.alarm.h = self.ui.sp_ho.value()
        self.alarm.m = self.ui.sp_mi.value()
        self.ui.lbl_alarm.setText(f"{'%0.2d' % self.alarm.h}:{'%0.2d' % self.alarm.m}")

    def disable_alarm(self):
        self.ui.btn_alarm_on.show()
        self.ui.btn_alarm_off.hide()
        self.alarm.terminate()
        self.ui.lbl_alarm.setText("00:00")

if __name__ == "__main__":
    app = QApplication([])
    window = Timer()
    sys.exit(app.exec())
