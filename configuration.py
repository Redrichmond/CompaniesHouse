#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Config.py: Config window."""

__author__ = "Victor H. Villalobos B."
__copyright__ = "Copyright 2015"

import configparser

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from wConfiguration import Ui_Dialog


class wConfiguration(QDialog, Ui_Dialog):
    signalUpdate = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(wConfiguration, self).__init__(parent)
        self.setupUi(self)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.lineApiKey.setText(self.config['Default']['ApiKey'])

    @pyqtSlot()
    def on_btnSave_clicked(self):
        self.config['Default']['ApiKey'] = self.lineApiKey.text()
        with open('config.ini', 'w') as configfile:  # save
            self.config.write(configfile)
        self.signalUpdate.emit(True)
        self.close()
