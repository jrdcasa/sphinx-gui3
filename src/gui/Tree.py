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
from PyQt5.QtCore import pyqtSlot, QDir
from src.pycore.app_utils import APP_PATH


class Tree(QtWidgets.QTreeView):

    # ---------------------------------
    def __init__(self, parent=None):

        super(Tree, self).__init__(parent)
        # ---
        self.content = None
        self.indexItem = None
        # ---
        self.setMaximumWidth(200)
        self.clicked.connect(self.on_treeview_clicked)

    # ---------------------------------
    def assign_content(self, content):
        self.content = content
        self.content.tree = self

    # ---------------------------------
    def reload(self):

        # ---Link the tree to a model
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(self.content.source_dir_path)
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
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

    # ---------------------------------
    @pyqtSlot(QtCore.QModelIndex)
    def on_treeview_clicked(self, index):

        indexItem = self.model().index(index.row(), 0, index.parent())
        # ---
        # cJ fileName = str(self.model().fileName(indexItem))
        filePath = str(self.model().filePath(indexItem))
        # ---
        if os.path.isfile(filePath):
            main_win = self.parent().parent()
            main_win.open_file(filePath, is_from_new_project=False)

        self.indexItem = indexItem

    # ---------------------------------
    @pyqtSlot(QtCore.QModelIndex)
    def on_treeview_clicked2(self, index):

        indexItem = self.model().index(index.row(), 0, index.parent())
        # ---
        # cJ fileName = str(self.model().fileName(indexItem))
        filePath = str(self.model().filePath(indexItem))
        # ---
        if os.path.isfile(filePath):
            main_win = self.parent().parent()
            main_win.open_file(filePath, is_from_new_project=False)

        self.indexItem = indexItem

    # ---------------------------------
    def menu_context_tree(self, point):

        # We build the menu.
        menu = QtWidgets.QMenu()
        action_0 = menu.addAction("Create new folder...")
        menu.addSeparator()
        action_1 = menu.addAction("Open Folder...")
        menu.addSeparator()
        action_2 = menu.addAction("Remove Folder...")
        menu.addSeparator()
        menu.addAction("Cancel")

        action_0.triggered.connect(self.create_new_folder)
        action_1.triggered.connect(self.open_folder)
        action_2.triggered.connect(self.remove_folder)

        menu.exec_(self.mapToGlobal(point))

    # ---------------------------------
    def create_new_folder(self):

        # Get current directory
        directory = self.content.source_dir_path
        if not directory:
            directory = os.getcwd()
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder', directory)

    # ---------------------------------
    def open_folder(self):

        # ---
        directory = self.content.source_dir_path
        if not directory: directory = APP_PATH
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                              directory=directory,
                                                              caption='Open folder')
        # ---
        if dir_path:
            self.content.set_source_dir(dir_path)
            main_win = self.parent().parent()

    # ---------------------------------
    def remove_folder(self):

        self.indexItem = self.selectedIndexes()[0]

        if self.indexItem is None:
                em = QtWidgets.QErrorMessage(self)
                em.showMessage("First select an item !!!")
                return

        filePath = str(self.model().filePath(self.indexItem))

        qm = QtWidgets.QMessageBox()
        qm.setIcon(QtWidgets.QMessageBox.Warning)
        qm.setWindowTitle("Confirm")
        reply = qm.question(self, '', "Are you sure to remove {} folder/file? "
                                      "\n============================"
                                      "\n(THIS TASK CANNOT BE UNDONE)"
                                      "\n============================".format(filePath), qm.Yes | qm.No)
        if reply == qm.Yes:

            try:
                if os.path.isdir(filePath):
                    os.rmdir(filePath)
                else:
                    os.remove(filePath)
                m = "File or folder\n {}\n HAS BEEN DELETED".format(filePath)
                QtWidgets.QMessageBox.about(self, 'Info', m)
            except:
                m = "File or folder\n {}\n CANNOT BE DELETED".format(filePath)
                QtWidgets.QMessageBox.about(self, 'Info', m)
