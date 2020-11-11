from PyQt5.QtWidgets import QCompleter
from PyQt5 import QtCore
import keyword

class MyCompleter(QCompleter):
	insertText = QtCore.pyqtSignal(str)

	def __init__(self, parent=None):
		QCompleter.__init__(self, keyword.kwlist, parent)
		self.setCompletionMode(QCompleter.PopupCompletion)
		self.highlighted.connect(self.setHighlighted)
		self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

	def setHighlighted(self, text):
		self.lastSelected = text

	def getSelected(self):
		return self.lastSelected

	def update(self, kwlist):
		newlist = keyword.kwlist+kwlist
		model = QtCore.QStringListModel(newlist, self)
		self.setModel(model)