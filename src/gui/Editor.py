"""
--------------------------------------------------------------------------
Copyright (C) 2017-2020 Lukasz Laba <lukaszlaba@gmail.com.pl>

This file is part of Tebe.

Tebe is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Tebe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tebe; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
"""

from PyQt5 import QtGui, QtCore, QtWidgets


class Editor(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        # ---
        self.document = None
        # ---
        self.setMinimumWidth(550)
        # ---
        self._setup()

    def assign_document(self, document):
        self.document = document

    def _setup(self):
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)

    def load_document(self):
        if self.document.has_data():
            self.setPlainText(self.document.get_text_content())
        else:
            self.clear()

    def get_text_content(self):
        text = self.toPlainText()
        # text = unicode(text)
        return text

    def get_scroll_relposition(self):
        absposition = self.verticalScrollBar().value()
        absmaximum = self.verticalScrollBar().maximum()
        if absmaximum != 0:
            relposition = 1.0 * absposition / absmaximum
        else:
            relposition = 0.0
        return relposition
