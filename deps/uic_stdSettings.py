#
# uic_stdSettings.py - STDF Viewer
# 
# Author: noonchen - chennoon233@foxmail.com
# Created Date: August 11th 2020
# -----
# Last Modified: Thu Dec 09 2021
# Modified By: noonchen
# -----
# Copyright (c) 2020 noonchen
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#



import sys
import platform
from random import choice
from copy import deepcopy
from .ui.ImgSrc_svg import ImgDict
# pyqt5
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTranslator
from .ui.stdfViewer_settingsUI import Ui_Setting
# pyside2
# from PySide2 import QtWidgets, QtGui
# from PySide2.QtCore import QTranslator
# from .ui.stdfViewer_settingsUI_side2 import Ui_Setting
# pyside6
# from PySide6 import QtWidgets, QtGui
# from PySide6.QtCore import QTranslator
# from .ui.stdfViewer_settingsUI_side6 import Ui_Setting


# simulate a Enum in python
class Tab(tuple): __getattr__ = tuple.index
tab = Tab(["Info", "Trend", "Histo", "Bin"])

isMac = platform.system() == 'Darwin'

indexDic_sigma = {0: "",
                  1: "3", 
                  2: "3, 6", 
                  3: "3, 6, 9"}
indexDic_sigma_reverse = {v:k for k, v in indexDic_sigma.items()}

indexDic_notation = {0: "G",
                     1: "F",
                     2: "E"}
indexDic_notation_reverse = {v:k for k, v in indexDic_notation.items()}

indexDic_lang = {0: "English",
                 1: "简体中文"}
indexDic_lang_reverse = {v:k for k, v in indexDic_lang.items()}

indexDic_sortby = {0: "Original",
                   1: "Number",
                   2: "Name"}
indexDic_sortby_reverse = {v:k for k, v in indexDic_sortby.items()}

rHEX = lambda: "#"+"".join([choice('0123456789ABCDEF') for j in range(6)])

class colorBtn(QtWidgets.QWidget):
    def __init__(self, parent=None, name="", num=None):
        super().__init__(parent=parent)
        self.name = name
        self.num = num
        self.setObjectName(self.name)
        self.hLayout = QtWidgets.QHBoxLayout(self)
        self.hLayout.setSpacing(5)
        fontsize = 12 if isMac else 10
        squaresize = 25 if isMac else 20
        # label
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.name)
        self.label.setStyleSheet("font: {0}pt Courier".format(fontsize))
        self.hLayout.addWidget(self.label)
        # color square
        self.square = QtWidgets.QWidget(self)
        self.square.setFixedSize(squaresize, squaresize)
        self.square.setStyleSheet("border:1px solid #000000;")
        self.hLayout.addWidget(self.square)
        self.square.mouseReleaseEvent = self.showPalette
        # spacer to avoid label from leaving button when resizing
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.hLayout.addItem(spacerItem)
        
    def setColor(self, qcolor):
        self.square.setStyleSheet("border:1px solid #000000; background-color:%s;"%str(qcolor.name()))
        # palette = self.square.palette()
        # palette.setColor(QtGui.QPalette.Background, qcolor)
        # self.square.setPalette(palette)
        # self.square.setAutoFillBackground(True)        
    
    def getHEXColor(self):
        qcolor = self.square.palette().button().color()
        return str(qcolor.name())
    
    def setName(self, name):
        self.name = name
        self.label.setText(self.name)
        
    def setNum(self, num):
        self.num = num
        
    def showPalette(self, event):
        currentColor = self.square.palette().button().color()
        color = QtWidgets.QColorDialog.getColor(parent=self, initial=currentColor)
        if color.isValid():
            self.setColor(color)
        else:
            self.setColor(currentColor)


class stdfSettings(QtWidgets.QDialog):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.translator = QTranslator(self)
        if self.parent: self.originalParams = deepcopy(self.parent.settingParams)
        self.settingsUI = Ui_Setting()
        self.settingsUI.setupUi(self)
        self.settingsUI.Confirm.clicked.connect(self.applySettings)
        self.settingsUI.Cancel.clicked.connect(self.close)
        self.settingsUI.lineEdit_binCount.setValidator(QtGui.QIntValidator(1, 1000, self))
        self.settingsUI.lineEdit_cpk.setValidator(QtGui.QDoubleValidator(self))
        
        self.settingsUI.settingBox.setItemIcon(0, QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(ImgDict["table"], format = 'SVG'))))
        self.settingsUI.settingBox.setItemIcon(1, QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(ImgDict["tab_trend"], format = 'SVG'))))
        self.settingsUI.settingBox.setItemIcon(2, QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(ImgDict["tab_histo"], format = 'SVG'))))
        self.settingsUI.settingBox.setItemIcon(3, QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(ImgDict["color_palette"], format = 'SVG'))))
                
        
    def initWithParentParams(self):
        # trend
        self.settingsUI.showHL_trend.setChecked(self.originalParams.showHL_trend)
        self.settingsUI.showLL_trend.setChecked(self.originalParams.showLL_trend)
        self.settingsUI.showHSpec_trend.setChecked(self.originalParams.showHSpec_trend)
        self.settingsUI.showLSpec_trend.setChecked(self.originalParams.showLSpec_trend)
        self.settingsUI.showMedian_trend.setChecked(self.originalParams.showMed_trend)
        self.settingsUI.showMean_trend.setChecked(self.originalParams.showMean_trend)
        # histo
        self.settingsUI.showHL_histo.setChecked(self.originalParams.showHL_histo)
        self.settingsUI.showLL_histo.setChecked(self.originalParams.showLL_histo)
        self.settingsUI.showHSpec_histo.setChecked(self.originalParams.showHSpec_histo)
        self.settingsUI.showLSpec_histo.setChecked(self.originalParams.showLSpec_histo)
        self.settingsUI.showMedian_histo.setChecked(self.originalParams.showMed_histo)
        self.settingsUI.showMean_histo.setChecked(self.originalParams.showMean_histo)
        self.settingsUI.showGaus_histo.setChecked(self.originalParams.showGaus_histo)
        self.settingsUI.showBoxp_histo.setChecked(self.originalParams.showBoxp_histo)
        self.settingsUI.lineEdit_binCount.setText(str(self.originalParams.binCount))
        self.settingsUI.sigmaCombobox.setCurrentIndex(indexDic_sigma_reverse.get(self.originalParams.showSigma, 0))
        # general
        self.settingsUI.langCombobox.setCurrentIndex(indexDic_lang_reverse.get(self.originalParams.language, 0))
        self.settingsUI.notationCombobox.setCurrentIndex(indexDic_notation_reverse.get(self.originalParams.dataNotation, 0))
        self.settingsUI.precisionSlider.setValue(self.originalParams.dataPrecision)
        self.settingsUI.checkCpkcomboBox.setCurrentIndex(0 if self.originalParams.checkCpk else 1)
        self.settingsUI.lineEdit_cpk.setText(str(self.originalParams.cpkThreshold))
        self.settingsUI.sortTestListComboBox.setCurrentIndex(indexDic_sortby_reverse.get(self.originalParams.sortTestList, 0))
        # color
        for (orig_dict, layout) in [(self.originalParams.siteColor, self.settingsUI.gridLayout_site_color),
                                    (self.originalParams.sbinColor, self.settingsUI.gridLayout_sbin_color),
                                    (self.originalParams.hbinColor, self.settingsUI.gridLayout_hbin_color)]:
            for i in range(layout.count()):
                cB = layout.itemAt(i).widget()
                orig_color = orig_dict.get(cB.num, rHEX())
                cB.setColor(QtGui.QColor(orig_color))
            
        
    def currentColorDict(self, get=True, group=""):
        if get:
            # get color dict from current settings
            obj = self.originalParams
        else:
            # apply color dict setting
            obj = self.parent.settingParams
        
        if group == "site": 
            layout = self.settingsUI.gridLayout_site_color
            color_dict = obj.siteColor
        elif group == "sbin": 
            layout = self.settingsUI.gridLayout_sbin_color
            color_dict = obj.sbinColor
        elif group == "hbin": 
            layout = self.settingsUI.gridLayout_hbin_color
            color_dict = obj.hbinColor
        else: 
            layout = None
            color_dict = {}
            
        if layout:
            for i in range(layout.count()):
                cB = layout.itemAt(i).widget()
                num = cB.num
                hex = cB.getHEXColor()
                color_dict[num] = hex
        if get: return color_dict
                            
    
    def updateSettings(self):
        # trend
        self.parent.settingParams.showHL_trend = self.settingsUI.showHL_trend.isChecked()
        self.parent.settingParams.showLL_trend = self.settingsUI.showLL_trend.isChecked()
        self.parent.settingParams.showHSpec_trend = self.settingsUI.showHSpec_trend.isChecked()
        self.parent.settingParams.showLSpec_trend = self.settingsUI.showLSpec_trend.isChecked()
        self.parent.settingParams.showMed_trend = self.settingsUI.showMedian_trend.isChecked()
        self.parent.settingParams.showMean_trend = self.settingsUI.showMean_trend.isChecked()
        # histo
        self.parent.settingParams.showHL_histo = self.settingsUI.showHL_histo.isChecked()
        self.parent.settingParams.showLL_histo = self.settingsUI.showLL_histo.isChecked()
        self.parent.settingParams.showHSpec_histo = self.settingsUI.showHSpec_histo.isChecked()
        self.parent.settingParams.showLSpec_histo = self.settingsUI.showLSpec_histo.isChecked()
        self.parent.settingParams.showMed_histo = self.settingsUI.showMedian_histo.isChecked()
        self.parent.settingParams.showMean_histo = self.settingsUI.showMean_histo.isChecked()
        self.parent.settingParams.showGaus_histo = self.settingsUI.showGaus_histo.isChecked()
        self.parent.settingParams.showBoxp_histo = self.settingsUI.showBoxp_histo.isChecked()
        self.parent.settingParams.binCount = int(self.settingsUI.lineEdit_binCount.text())
        self.parent.settingParams.showSigma = indexDic_sigma[self.settingsUI.sigmaCombobox.currentIndex()]
        # General
        self.parent.settingParams.language = indexDic_lang[self.settingsUI.langCombobox.currentIndex()]
        self.parent.settingParams.dataNotation = indexDic_notation[self.settingsUI.notationCombobox.currentIndex()]
        self.parent.settingParams.dataPrecision = self.settingsUI.precisionSlider.value()
        self.parent.settingParams.checkCpk = (self.settingsUI.checkCpkcomboBox.currentIndex() == 0)
        self.parent.settingParams.cpkThreshold = float(self.settingsUI.lineEdit_cpk.text())
        self.parent.settingParams.sortTestList = indexDic_sortby[self.settingsUI.sortTestListComboBox.currentIndex()]
        # color
        for group in ["site", "sbin", "hbin"]:
            self.currentColorDict(get=False, group=group)
        
        self.parent.dumpConfigFile()
        
        
    def isTrendChanged(self):
        return not all([getattr(self.originalParams, attr) == getattr(self.parent.settingParams, attr) 
                        for attr in ["showHL_trend", "showLL_trend", "showHSpec_trend", "showLSpec_trend", "showMed_trend", "showMean_trend"]])
        
        
    def isHistoChanged(self):
        return not all([getattr(self.originalParams, attr) == getattr(self.parent.settingParams, attr) 
                        for attr in ["showHL_histo", "showLL_histo", "showHSpec_histo", "showLSpec_histo", "showMed_histo", "showMean_histo", 
                                     "showGaus_histo", "showBoxp_histo", "binCount", "showSigma"]])
        
         
    def isGeneralChanged(self):
        return not all([getattr(self.originalParams, attr) == getattr(self.parent.settingParams, attr) 
                        for attr in ["language", "dataNotation", "dataPrecision", "checkCpk", "cpkThreshold", "sortTestList"]])


    def isColorChanged(self):
        return not all([getattr(self.originalParams, attr) == getattr(self.parent.settingParams, attr) 
                        for attr in ["siteColor", "sbinColor", "hbinColor"]])
    
    
    def applySettings(self):
        if self.parent:
            # write setting to parent settings
            self.updateSettings()
            refreshTab = False
            refreshTable = False
            refreshList = False
            clearListBG = False
            refreshCursor = False
            retranslate = False
            if self.isTrendChanged() and (self.parent.ui.tabControl.currentIndex() == tab.Trend): 
                refreshTab = True
                
            if self.isHistoChanged() and (self.parent.ui.tabControl.currentIndex() == tab.Histo): 
                refreshTab = True
                
            if self.isGeneralChanged(): 
                if self.originalParams.language != self.parent.settingParams.language:
                    retranslate = True
                if self.originalParams.sortTestList != self.parent.settingParams.sortTestList:
                    refreshList = True
                if self.parent.ui.tabControl.currentIndex() != tab.Bin:
                    refreshTable = True
                    refreshCursor = True
                    # if raw data table is active, update as well
                    if (self.parent.ui.tabControl.currentIndex() == tab.Info) and (self.parent.ui.infoBox.currentIndex() == 2):
                        refreshTab = True
                    # if cpk threshold changed, clear listView backgrounds
                    if self.originalParams.cpkThreshold != self.parent.settingParams.cpkThreshold or self.originalParams.checkCpk != self.parent.settingParams.checkCpk:
                        clearListBG = True
                    
            if self.isColorChanged():
                refreshTab = True
                refreshTable = True
                
            if refreshTab: self.parent.updateTabContent(forceUpdate=True)
            if refreshTable: self.parent.updateStatTableContent()
            if refreshList: self.parent.refreshTestList()
            if clearListBG: self.parent.clearTestItemBG()
            if refreshCursor: self.parent.updateCursorPrecision()
            if retranslate: self.parent.changeLanguage()
                
            # need to update orignal params after updating parent settings
            self.originalParams = deepcopy(self.parent.settingParams)
        QtWidgets.QApplication.processEvents()
        self.close()
    
    
    def closeEvent(self, event):
        event.accept()
        
        
    def removeColorBtns(self):
        for layout in [self.settingsUI.gridLayout_site_color,
                       self.settingsUI.gridLayout_sbin_color,
                       self.settingsUI.gridLayout_hbin_color]:
            for i in range(layout.count())[::-1]:   # delete in reverse
                cB = layout.itemAt(i).widget()
                layout.removeWidget(cB)
                cB.deleteLater()
                cB.setParent(None)
    
    
    def initColorBtns(self):
        # site color picker
        site_color_group = self.settingsUI.site_groupBox
        site_gridLayout = self.settingsUI.gridLayout_site_color
        for i, siteNum in enumerate([-1]+[i for i in self.parent.availableSites]):
            siteName = f"Site {siteNum:<2}" if siteNum != -1 else "All Site"
            cB = colorBtn(parent=site_color_group, name=siteName, num=siteNum)
            row = i//3
            col = i % 3
            site_gridLayout.addWidget(cB, row, col)
            
        # sbin color picker
        sbin_color_group = self.settingsUI.sbin_groupBox
        sbin_gridLayout = self.settingsUI.gridLayout_sbin_color
        for i, sbin in enumerate([i for i in sorted(self.parent.SBIN_dict.keys())]):
            binName = f"SBIN {sbin:<2}"
            cB = colorBtn(parent=sbin_color_group, name=binName, num=sbin)
            row = i//3
            col = i % 3
            sbin_gridLayout.addWidget(cB, row, col)
            
        # hbin color picker
        hbin_color_group = self.settingsUI.hbin_groupBox
        hbin_gridLayout = self.settingsUI.gridLayout_hbin_color
        for i, hbin in enumerate([i for i in sorted(self.parent.HBIN_dict.keys())]):
            binName = f"HBIN {hbin:<2}"
            cB = colorBtn(parent=hbin_color_group, name=binName, num=hbin)
            row = i//3
            col = i % 3
            hbin_gridLayout.addWidget(cB, row, col)
                
    
    def showUI(self):
        if self.parent: 
            self.originalParams = deepcopy(self.parent.settingParams)
            self.initWithParentParams()
            currentTab = self.parent.ui.tabControl.currentIndex()
            if currentTab == 0: currentIndex = 0            # info tab
            elif currentTab == 1: currentIndex = 1          # trend tab
            elif currentTab == 2: currentIndex = 2          # histo tab
            else: currentIndex = 3                          # bin & wafer
            self.settingsUI.settingBox.setCurrentIndex(currentIndex)

        self.exec_()           
           
           
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    # test = stdfSettings()
    # w = colorBtn(name="All site", num=1)
    # w.show()
    sys.exit(app.exec_())
    
    
