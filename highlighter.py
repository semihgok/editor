from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat,QColor,QBrush
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
		QMessageBox, QTextEdit)
import re
import keyword

class Highlighter(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super(Highlighter, self).__init__(parent)
		self.compHighlightingRules = []
		self.userkw = ["hello"]


		keywordFormat = QTextCharFormat()
		keywordFormat.setForeground(QColor("#E21949"))
		keywordFormat.setFontWeight(QFont.Bold)
		keywords = ["as","else","from","elif","if","import","continue","except","break","in","is","global","finally","for",'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
		keywordPatterns = map(lambda x: "\\b"+x+"\\b",keywords)

		keywords3 = ["class","def","None","True","False","lambda"]

		keywordFormat2 = QTextCharFormat()
		keywordFormat2.setForeground(QColor("#e67e22"))
		keywordFormat2.setFontWeight(QFont.Bold)
		keywords2 = list(set(keyword.kwlist)-set(keywords+keywords3))+["self"]
		keywordPatterns2 = map(lambda x: "\\b"+x+"\\b",keywords2)

		keywordFormat3 = QTextCharFormat()
		keywordFormat3.setForeground(QColor("#1989E2"))
		keywordFormat3.setFontWeight(QFont.Bold)
		keywordPatterns3 = map(lambda x: "\\b"+x+"\\b",keywords3)

		self.highlightingRules = [(QRegExp(pattern), keywordFormat) for pattern in keywordPatterns]
		self.highlightingRules += [(QRegExp(pattern), keywordFormat2) for pattern in keywordPatterns2]
		self.highlightingRules += [(QRegExp(pattern), keywordFormat3) for pattern in keywordPatterns3]

		# classFormat = QTextCharFormat()
		# classFormat.setFontWeight(QFont.Bold)
		# classFormat.setForeground(Qt.darkMagenta)
		# self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
		# 		classFormat))

		singleLineCommentFormat = QTextCharFormat()
		singleLineCommentFormat.setForeground(QColor("#ccc"))
		self.highlightingRules.append((QRegExp("^#.*"),
				singleLineCommentFormat))

		self.multiLineCommentFormat = QTextCharFormat()
		self.multiLineCommentFormat.setForeground(Qt.red)

		self.inheritCommentFormat = QTextCharFormat()
		self.inheritCommentFormat.setFontItalic(True)
		self.inheritCommentFormat.setForeground(QColor("#3FC926"))

		self.customFormat = QTextCharFormat()
		self.customFormat.setFontItalic(True)
		self.customFormat.setForeground(QColor("#e67e22"))

		quotationFormat = QTextCharFormat()
		quotationFormat.setForeground(QColor("#DA3B01"))
		self.highlightingRules.append((QRegExp("\".*\""), quotationFormat))

		functionFormat = QTextCharFormat()
		functionFormat.setFontItalic(True)
		functionFormat.setForeground(QColor("#3FC926"))
		self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
				functionFormat))


		self.commentStartExpression = QRegExp('/\\*')
		self.commentEndExpression = QRegExp('\\*/')

		self.inheritStartExpression = QRegExp('class [A-Za-z0-9_]+\(')
		self.inheritEndExpression = QRegExp(')')

	def highlightBlock(self, text):
		for pattern, format in self.highlightingRules:
			index = pattern.indexIn(text)
			while index > -1:
				length = pattern.matchedLength()
				self.setFormat(index, length, format)
				index = pattern.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		startIndex = 0
		if self.previousBlockState() != 1:
			startIndex = self.commentStartExpression.indexIn(text)


		while startIndex >= 0:
			endIndex = self.commentEndExpression.indexIn(text, startIndex)
			if endIndex == -1:
				self.setCurrentBlockState(1)
				commentLength = len(text) - startIndex
			else:
				commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

			self.setFormat(startIndex, commentLength,
					self.multiLineCommentFormat)
			startIndex = self.commentStartExpression.indexIn(text,
					startIndex + commentLength);


		self.setCurrentBlockState(0)

		r = re.findall("class (.*?)\(",text)
		if(r):
			r2 = re.findall("class "+r[0]+"\((.*?)\)",text)
			start = len(r[0])+7
			length = len(text)-(len(r[0])+7)
			if r2:
				if r[0] not in self.userkw:
					self.userkw.append(r[0])
				start = len(r[0])+7
				length = len(r2[0])
			self.setFormat(start, length, self.inheritCommentFormat)

		self.setCurrentBlockState(0)

		r = re.findall("def (.*?)\(",text)
		if r:
			if(len(r[0])>0):
				r2 = re.findall("def "+r[0]+"\((.*?)\)",text)
				split = text.split(r[0])
				start2 = len(split[0])+len(r[0])+1
				length2 = len(text)-(len(split[0]))
				if r2:
					start2 = len(split[0])+len(r[0])+1
					length2 = len(r2[0])
				self.setFormat(start2, length2, self.customFormat)
		