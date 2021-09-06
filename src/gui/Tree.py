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

import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot


class Tree(QtWidgets.QTreeView):

	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)
		# ---
		self.content = None
		# ---
		self.setMaximumWidth(200)
		self.clicked.connect(self.on_treeview_clicked)

	def assign_content(self, content):
		self.content = content
		self.content.tree = self

	def reload(self):
		# ---Link the tree to a model
		model = QtWidgets.QFileSystemModel()
		model.setRootPath(self.content.source_dir_path)
		model.setNameFilters(["*.md", "*.rst", "*.py"])
		self.setModel(model)
		# ---Set the tree's index to the root of the model
		indexRoot = model.index(model.rootPath())
		self.setRootIndex(indexRoot)
		# ---Hide tree size and date columns
		self.hideColumn(1)
		self.hideColumn(2)
		self.hideColumn(3)
		# ---Hide tree header
		self.setHeaderHidden(True)

	@pyqtSlot(QtCore.QModelIndex)
	def on_treeview_clicked(self, index):

		indexItem = self.model().index(index.row(), 0, index.parent())
		# ---
		# cJ fileName = str(self.model().fileName(indexItem))
		filePath = str(self.model().filePath(indexItem))
		# ---
		if os.path.isfile(filePath):
			main_win = self.parent().parent()
			main_win.openFile(filePath, is_from_new_project=False)
