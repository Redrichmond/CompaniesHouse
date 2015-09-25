__author__ = 'Viktor'

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from wAbout import Ui_Dialog


class wAbout(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(wAbout, self).__init__(parent)
        self.setupUi(self)


    @pyqtSlot()
    def on_lblWeb_clicked(self):
        print('hola')