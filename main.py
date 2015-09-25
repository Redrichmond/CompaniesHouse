#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main.py: metodo main."""

__author__ = "Victor H. Villalobos B."
__copyright__ = "Copyright 2015"

import sys
import subprocess
import os
import configparser

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from wMain import Ui_MainWindow
from configuration import wConfiguration
from importer import Importer
from about import wAbout


class wMain(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(wMain, self).__init__(parent)
        self.setupUi(self)
        self.statusbar.showMessage('Utility for CompaniesHouse.gov.uk import')
        self.updateApiKey()
        if getattr(sys, 'frozen', False):
            # frozen
            self.outputDir = os.path.dirname(sys.executable) + '\\output\\'
            self.dirBase = os.path.dirname(sys.executable)
        else:
            # unfrozen
            self.outputDir = os.path.dirname(os.path.realpath(__file__)) + '\\output\\'
            self.dirBase = os.path.dirname(os.path.realpath(__file__))
        #self.outputDir = os.path.dirname(os.path.realpath(__file__)) + '\\output\\'

    def updateApiKey(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.apikey = self.config['Default']['ApiKey']

    @pyqtSlot()
    def on_btnFindImport_clicked(self):
        fileImport = QFileDialog.getOpenFileName(self, '', '', "Csv File (*.csv);; All files(*.*)")
        self.lineImport.setText(fileImport[0])

    @pyqtSlot()
    def on_btnFindOutput_clicked(self):
        fileOutput = QFileDialog.getSaveFileName(self, '', '', "Csv File (*.csv);; All files(*.*)")
        self.lineOutput.setText(fileOutput[0])

    @pyqtSlot()
    def on_btnStart_clicked(self):
        if hasattr(self, 'imp'):
            if (not (self.imp.isRunning())) and (self.imp.pause == False):
               self.activate()
            elif((self.imp.isRunning()) and (self.imp.pause == True)):
                self.imp.setPause(False)
                self.btnStart.setEnabled(False)
                self.btnStop.setEnabled(True)
                self.btnPause.setEnabled(True)
                self.setWindowTitle('Companies House Web Scrapping Tool')
            else:
                self.activate()
        else:
            self.activate()


    def activate(self):
        self.setWindowTitle('Companies House Web Scrapping Tool')
        if not (len(self.lineImport.text()) > 1):
            self.lineImport.setText(QDir.fromNativeSeparators(self.dirBase + '\\input\\import.csv'))
        if os.path.isfile(self.lineImport.text()):
            self.progressBar.setValue(0)
            self.imp = Importer(self, self.apikey, self.lineImport.text(),
            self.dirBase + '\\output\\output.csv')
            self.imp.updateSignal.connect(self.progressBar.setValue)
            self.imp.maxSignal.connect(self.setRange)
            self.imp.closeSignal.connect(self.finished)
            self.imp.start()
            self.btnStart.setEnabled(False)
            self.btnStop.setEnabled(True)
            self.btnPause.setEnabled(True)
        else:
            QMessageBox.warning(self,'Error', self.lineImport.text() + "doesn't exist")

    def setRange(self, end):
        self.progressBar.setRange(0, end)


    def finished(self):
        subprocess.call(['explorer', QDir.toNativeSeparators(self.outputDir)])
        self.imp.terminate()
        self.btnPause.setEnabled(False)
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
        self.setWindowTitle('PROCESS COMPLETED')
        QMessageBox.information(self, 'Process', 'The process has successfully finished')


    @pyqtSlot()
    def on_btnPause_clicked(self):
        if self.imp.isRunning():
            self.imp.setPause(True)
            self.btnPause.setEnabled(False)
            self.btnStart.setEnabled(True)
            self.imp.save(True)

    @pyqtSlot()
    def on_btnStop_clicked(self):
        reply = QMessageBox.question(self, "Warning",
                                     "really you want to stop the import unfinished?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.imp.save(True)
            subprocess.call(['explorer', QDir.toNativeSeparators(self.outputDir)])
            self.imp.terminate()
            self.btnStop.setEnabled(False)
            self.btnPause.setEnabled(False)
            self.btnStart.setEnabled(True)
            if self.imp.isFinished():
                print('cerrando')

    @pyqtSlot()
    def on_actionConfiguration_triggered(self):
        window = wConfiguration()
        window.signalUpdate.connect(self.updateApiKey)
        window.exec_()

    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_actionAbout_this_triggered(self):
        window = wAbout()
        window.exec_()

    @pyqtSlot()
    def on_actionOpen_Log_triggered(self):
        subprocess.call(['notepad', QDir.toNativeSeparators(os.path.dirname(os.path.realpath(__file__)) + '/import.log')])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vMain = wMain()
    vMain.show()
    sys.exit(app.exec_())
