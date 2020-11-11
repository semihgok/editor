from PyQt5.QtWidgets import QCompleter, QPlainTextEdit,QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from MyCompleter import *
import time

class AwesomeTextEdit(QPlainTextEdit):
	def __init__(self, parent=None):
		super(AwesomeTextEdit, self).__init__(parent)
		self.completer = MyCompleter()
		self.completer.setWidget(self)
		self.completer.insertText.connect(self.insertCompletion)
		self.key = None
		self.block = False
		self.last = []
		self.filePath = None
		self.setStyleSheet("background-color: #323232;color:white;")

	def insertCompletion(self, completion):
		tc = self.textCursor()
		extra = (len(completion) - len(self.completer.completionPrefix()))
		#print(completion)
		tc.movePosition(QTextCursor.Left)
		tc.select(tc.WordUnderCursor)
		tc.insertText(tc.selectedText().replace(tc.selectedText(),completion))
		self.setTextCursor(tc)
		self.completer.popup().hide()

	def focusInEvent(self, event):
		if self.completer:
			self.completer.setWidget(self)
		QPlainTextEdit.focusInEvent(self, event)

	def keyPressEvent(self, event):
		self.key = event.key()
		if event.key() == QtCore.Qt.Key_Backtab:
			cur = self.textCursor()
			pos = cur.position()
			anchor = cur.anchor()
			cur.setPosition(pos) 
			cur.setPosition(pos-1,QtGui.QTextCursor.KeepAnchor)
			
			if str(cur.selectedText()) == "\t":
				cur.removeSelectedText()
				cur.setPosition(anchor-1)
				cur.setPosition(pos-1,QtGui.QTextCursor.KeepAnchor)
			else:
				cur.setPosition(anchor) 
				cur.setPosition(anchor-1,QtGui.QTextCursor.KeepAnchor)
				if str(cur.selectedText()) == "\t":
					cur.removeSelectedText()
					cur.setPosition(anchor-1)
					cur.setPosition(pos-1,QtGui.QTextCursor.KeepAnchor)
				else:
					cur.setPosition(anchor)
					cur.setPosition(pos,QtGui.QTextCursor.KeepAnchor)
		tc = self.textCursor()
		if event.key() == Qt.Key_Return and self.completer.popup().isVisible():
			self.completer.insertText.emit(self.completer.getSelected())
			self.completer.setCompletionMode(QCompleter.PopupCompletion)
			return

		QPlainTextEdit.keyPressEvent(self, event)
		tc.select(QTextCursor.WordUnderCursor)
		cr = self.cursorRect()

		keylist = [Qt.Key_Down,Qt.Key_Up,Qt.Key_Right,Qt.Key_Left]

		if len(tc.selectedText()) > 0 and tc.selectedText() != self.completer.currentCompletion() and event.key() not in keylist:
			self.completer.setCompletionPrefix(tc.selectedText())
			popup = self.completer.popup()
			popup.setCurrentIndex(self.completer.completionModel().index(0,0))
			cr.setWidth(self.completer.popup().sizeHintForColumn(0) 
			+ self.completer.popup().verticalScrollBar().sizeHint().width())
			self.completer.complete(cr)
		else:
			self.completer.popup().hide()

	def add_indent(self):
		cursor = self.textCursor()
		line = cursor.blockNumber()
		split = self.toPlainText().split("\n")
		last = split[line-1]
		count = last.count("\t")

		if last.endswith(":") and self.key == Qt.Key_Return:
			self.key = None
			self.insertPlainText("\t"*(count+1))

		elif self.key == Qt.Key_Return:
			self.key = None
			count = last.count("\t")
			self.insertPlainText("\t"*(count))
			

	def autoComplete():
		pass


	def add_kw(self,a):
		if a != self.last:
			self.completer.update(a)
