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

from PyQt5 import QtCore, QtWebEngineWidgets


class Preview(QtWebEngineWidgets.QWebEngineView):

	def __init__(self, parent=None):

		super(Preview, self).__init__(parent)
		# ---
		self.scroll_fixed_position = False
		# ---
		self.page().loadFinished.connect(self.scroll_to_fixed_position)

	def show_html(self, path):
		self.load(QtCore.QUrl.fromLocalFile(path))

	def show_url(self, link):
		self.load(QtCore.QUrl(link))

	def scroll_fix(self):
		if self.page().scrollPosition().y() != 0:
			self.scroll_fixed_position = self.scroll_get_position()

	def scroll_get_position(self):
		return self.page().scrollPosition().y()

	def scroll_up(self):
		self.scroll_fixed_position = 1
		self.scroll_to_fixed_position()

	def scroll_to_fixed_position(self):
		if self.scroll_fixed_position:
			self.scroll_to_absposition(self.scroll_fixed_position)

	def scroll_to_absposition(self, position):
		QtCore.QPoint(0, position)
		self.scroll_fixed_position = position
		# can't find method like page().srollTo() so runJavaScript used
		self.page().runJavaScript('window.scrollTo(0, %s);' % position)

	def scroll_to_relposition(self, relosition):
		absposition = relosition * self.page().contentsSize().height()
		self.scroll_to_absposition(absposition)
