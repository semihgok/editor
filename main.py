# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled3.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

#
#
# Tree View seçilen dosyayı göster
#
#

from PyQt5 import QtCore, QtGui, QtWidgets
import keyword
import highlighter
import textEdit
import os
from functools import partial

class MyQFileSystemModel(QtWidgets.QFileSystemModel):

	def headerData(self, section, orientation, role):
		if section == 0:
			return "Dosyalar"
		else:
			return super(QtWidgets.QFileSystemModel, self).headerData(section, orientation, role)


class Ui_MainWindow(object):
	def __init__(self):
		self.tabs = {}
		self.activeTab = None

	def openFolder_(self):
		filenames = self.selectFolder()
		self.fileSystemModel.setReadOnly(False)
		self.fileSystemModel.headerData(0, QtCore.Qt.Horizontal, QtCore.Qt.TextAlignmentRole)
		root = self.fileSystemModel.setRootPath(filenames[0])
		self.fileViewer.setModel(self.fileSystemModel)
		self.fileViewer.setRootIndex(root)
		for i in range(1,self.fileSystemModel.columnCount()):
			self.fileViewer.hideColumn(i)



	def selectFolder(self):
		dlg = QtWidgets.QFileDialog()
		dlg.setDirectory(QtCore.QDir.currentPath())
		dlg.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
		filenames = str

		if dlg.exec_():
			filenames = dlg.selectedFiles()
			return filenames
			

	def selectFile(self):
		dlg = QtWidgets.QFileDialog()
		dlg.setNameFilters(["Python Files (*.py)"])
		dlg.selectNameFilter("Python Files (*.py)")
		filenames = str

		if dlg.exec_():
			filenames = dlg.selectedFiles()
			f = open(filenames[0],"r")
			r = f.read()
			self.createTab(os.path.basename(filenames[0]),r,filePath=filenames[0])
			f.close()

	def saveFile(self):
		current = self.tabWidget.currentWidget()
		editor = current.findChild(textEdit.AwesomeTextEdit)
		if editor.filePath:
			f = open(editor.filePath,"w")
			f.write(editor.toPlainText())
			f.close()
		else:
			currentIndex = self.tabWidget.currentIndex()
			text = self.tabWidget.tabText(currentIndex)
			name = QtWidgets.QFileDialog.getSaveFileName(caption="Save File",directory=text+".py")
			f = open(name[0],"w")
			f.write(editor.toPlainText())
			f.close()
			self.tabWidget.setTabText(currentIndex,os.path.basename(name[0]))
			editor.filepath = name[0]


	def getAllTabTitles(self):
		return [self.tabWidget.tabText(i) for i in range(self.tabWidget.count())]



	def createTab(self,tabTitle="untitled",editorText=None,filePath = None):
		tab = QtWidgets.QWidget()
		gridLayout = QtWidgets.QGridLayout(tab)
		gridLayout.setContentsMargins(0, 0, 0, 0)
		verticalLayout = QtWidgets.QVBoxLayout()

		editor = textEdit.AwesomeTextEdit(tab)
		editor.setLineWrapMode(editor.NoWrap)
		if editorText != None:
			editor.insertPlainText(str(editorText))
		editor.setTabStopWidth(editor.fontMetrics().width(' ') * 8)
		editor.setObjectName("editor")
		editor.filePath = filePath
		editor.setTabStopDistance(QtGui.QFontMetricsF(editor.font()).width(' ') * 8)
		self.highlighter = highlighter.Highlighter(editor.document())
		editor.textChanged.connect(editor.add_indent)
		editor.textChanged.connect(partial(editor.add_kw,self.highlighter.userkw))

		new_font = QtGui.QFont("Consolas", 12)
		new_font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing,1.2)
		editor.setFont(new_font)
		verticalLayout.addWidget(editor)
		gridLayout.addLayout(verticalLayout, 0, 0, 1, 1)

		count = 1
		title = tabTitle
		while True:
			if title in self.getAllTabTitles():
				title = tabTitle+"("+str(count)+")"
				count += 1
				continue
			break
		self.tabWidget.addTab(tab, title)
		self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)

	def createNewFile(self):
		self.createTab()

	def tabChange(self,i):
		self.activeTab = i

	def removeTab(self,i):
		self.tabWidget.removeTab(i)


	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(761, 557)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setSpacing(0)
		self.gridLayout.setObjectName("gridLayout")
		self.splitter = QtWidgets.QSplitter(self.centralwidget)
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		self.splitter.setObjectName("splitter")
		self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
		self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
		self.leftLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
		self.leftLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
		self.leftLayout.setContentsMargins(0, 0, 0, 0)
		self.leftLayout.setSpacing(0)
		self.leftLayout.setObjectName("leftLayout")
		
		self.fileViewer = QtWidgets.QTreeView(self.horizontalLayoutWidget_2)
		self.fileViewer.setMaximumSize(QtCore.QSize(200, 16777215))
		self.fileViewer.setBaseSize(QtCore.QSize(0, 0))
		self.fileViewer.setObjectName("fileViewer")
		self.fileViewer.header().setDefaultSectionSize(1)
		self.leftLayout.addWidget(self.fileViewer)

		self.fileSystemModel = MyQFileSystemModel(self.fileViewer)

		self.horizontalLayoutWidget = QtWidgets.QWidget(self.splitter)
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.rightLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
		self.rightLayout.setContentsMargins(0, 0, 0, 0)
		self.rightLayout.setSpacing(0)
		self.rightLayout.setObjectName("rightLayout")

		self.tabWidget = QtWidgets.QTabWidget(self.horizontalLayoutWidget)
		self.tabWidget.setObjectName("tabWidget")
		self.tabWidget.setTabsClosable(True)
		#self.tabWidget.currentChanged.connect(self.tabChange)
		self.tabWidget.tabCloseRequested.connect(self.removeTab)
		self.rightLayout.addWidget(self.tabWidget)

		self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 761, 21))
		self.menubar.setObjectName("menubar")
		self.fileMenu = QtWidgets.QMenu(self.menubar)
		self.fileMenu.setObjectName("fileMenu")
		self.fontMenu = QtWidgets.QMenu(self.menubar)
		self.fontMenu.setObjectName("fontMenu")
		self.menuFont_Size = QtWidgets.QMenu(self.fontMenu)
		self.menuFont_Size.setObjectName("menuFont_Size")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.action2 = QtWidgets.QAction(MainWindow)
		self.action2.setObjectName("action2")
		self.action24 = QtWidgets.QAction(MainWindow)
		self.action24.setObjectName("action24")
		self.action32 = QtWidgets.QAction(MainWindow)
		self.action32.setObjectName("action32")
		self.font_8 = QtWidgets.QAction(MainWindow)
		self.font_8.setObjectName("font_8")
		self.font_10 = QtWidgets.QAction(MainWindow)
		self.font_10.setObjectName("font_10")
		self.font_12 = QtWidgets.QAction(MainWindow)
		self.font_12.setObjectName("font_12")
		self.font_14 = QtWidgets.QAction(MainWindow)
		self.font_14.setObjectName("font_14")
		self.font_16 = QtWidgets.QAction(MainWindow)
		self.font_16.setObjectName("font_16")
		self.font_18 = QtWidgets.QAction(MainWindow)
		self.font_18.setObjectName("font_18")
		self.font_20 = QtWidgets.QAction(MainWindow)
		self.font_20.setObjectName("font_20")
		self.font_22 = QtWidgets.QAction(MainWindow)
		self.font_22.setObjectName("font_22")
		self.font_24 = QtWidgets.QAction(MainWindow)
		self.font_24.setObjectName("font_24")
		self.font_26 = QtWidgets.QAction(MainWindow)
		self.font_26.setObjectName("font_26")
		self.font_28 = QtWidgets.QAction(MainWindow)
		self.font_28.setObjectName("font_28")
		self.font_30 = QtWidgets.QAction(MainWindow)
		self.font_30.setObjectName("font_30")
		self.font_32 = QtWidgets.QAction(MainWindow)
		self.font_32.setObjectName("font_32")
		self.font_34 = QtWidgets.QAction(MainWindow)
		self.font_34.setObjectName("font_34")
		self.font_36 = QtWidgets.QAction(MainWindow)
		self.font_36.setObjectName("font_36")

		self.newFile = QtWidgets.QAction(MainWindow)
		self.newFile.setObjectName("newFile")
		self.newFile.triggered.connect(self.createNewFile)

		self.openFile = QtWidgets.QAction(MainWindow)
		self.openFile.setObjectName("openFile")
		self.openFile.triggered.connect(self.selectFile)

		self.openFolder = QtWidgets.QAction(MainWindow)
		self.openFolder.setObjectName("openFolder")
		self.openFolder.triggered.connect(self.openFolder_)

		self.actionSave = QtWidgets.QAction(MainWindow)
		self.actionSave.setObjectName("actionSave")
		self.actionSave.triggered.connect(self.saveFile)

		self.fileMenu.addAction(self.newFile)
		self.fileMenu.addAction(self.openFile)
		self.fileMenu.addAction(self.openFolder)
		self.fileMenu.addAction(self.actionSave)
		self.menuFont_Size.addAction(self.font_8)
		self.menuFont_Size.addAction(self.font_10)
		self.menuFont_Size.addAction(self.font_12)
		self.menuFont_Size.addAction(self.font_14)
		self.menuFont_Size.addAction(self.font_16)
		self.menuFont_Size.addAction(self.font_18)
		self.menuFont_Size.addAction(self.font_20)
		self.menuFont_Size.addAction(self.font_22)
		self.menuFont_Size.addAction(self.font_24)
		self.menuFont_Size.addAction(self.font_26)
		self.menuFont_Size.addAction(self.font_28)
		self.menuFont_Size.addAction(self.font_30)
		self.menuFont_Size.addAction(self.font_32)
		self.menuFont_Size.addAction(self.font_34)
		self.menuFont_Size.addAction(self.font_36)
		self.fontMenu.addAction(self.menuFont_Size.menuAction())
		self.menubar.addAction(self.fileMenu.menuAction())
		self.menubar.addAction(self.fontMenu.menuAction())

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		#self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
		self.fileMenu.setTitle(_translate("MainWindow", "File"))
		self.fontMenu.setTitle(_translate("MainWindow", "Font"))
		self.menuFont_Size.setTitle(_translate("MainWindow", "Font Size"))
		self.action2.setText(_translate("MainWindow", "2"))
		self.action24.setText(_translate("MainWindow", "24"))
		self.action32.setText(_translate("MainWindow", "32"))
		self.font_8.setText(_translate("MainWindow", "8"))
		self.font_10.setText(_translate("MainWindow", "10"))
		self.font_12.setText(_translate("MainWindow", "12"))
		self.font_14.setText(_translate("MainWindow", "14"))
		self.font_16.setText(_translate("MainWindow", "16"))
		self.font_18.setText(_translate("MainWindow", "18"))
		self.font_20.setText(_translate("MainWindow", "20"))
		self.font_22.setText(_translate("MainWindow", "22"))
		self.font_24.setText(_translate("MainWindow", "24"))
		self.font_26.setText(_translate("MainWindow", "26"))
		self.font_28.setText(_translate("MainWindow", "28"))
		self.font_30.setText(_translate("MainWindow", "30"))
		self.font_32.setText(_translate("MainWindow", "32"))
		self.font_34.setText(_translate("MainWindow", "34"))
		self.font_36.setText(_translate("MainWindow", "36"))
		self.newFile.setText(_translate("MainWindow", "New File"))
		self.openFile.setText(_translate("MainWindow", "Open File"))
		self.openFolder.setText(_translate("MainWindow", "Open Folder"))
		self.actionSave.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

