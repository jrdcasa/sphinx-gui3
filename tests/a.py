import os

from PyQt5.QtCore import pyqtSlot, QDir, QModelIndex, QSize, QSortFilterProxyModel
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QMainWindow, QTreeView


class ProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._root_path = ""

    def filterAcceptsRow(self, source_row, source_parent):
        source_model = self.sourceModel()
        if self._root_path and isinstance(source_model, QFileSystemModel):
            root_index = source_model.index(self._root_path).parent()
            if root_index == source_parent:
                index = source_model.index(source_row, 0, source_parent)
                return index.data(QFileSystemModel.FilePathRole) == self._root_path
        return True

    @property
    def root_path(self):
        return self._root_path

    @root_path.setter
    def root_path(self, p):
        self._root_path = p
        self.invalidateFilter()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_treeview()
        self.setCentralWidget(self.treeView)

    def create_treeview(self):

        path = "/home/jramos/TMP"

        self.treeView = QTreeView()
        self.treeView.setMinimumSize(QSize(250, 0))
        self.treeView.setMaximumSize(QSize(250, 16777215))
        self.treeView.setObjectName("treeView")

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        root_index = self.dirModel.index(path).parent()

        self.proxy = ProxyModel(self.dirModel)
        self.proxy.setSourceModel(self.dirModel)
        self.proxy.root_path = path

        self.treeView.setModel(self.proxy)

        proxy_root_index = self.proxy.mapFromSource(root_index)
        self.treeView.setRootIndex(proxy_root_index)

        self.treeView.setHeaderHidden(True)
        self.treeView.clicked.connect(self.tree_click)

    @pyqtSlot(QModelIndex)
    def tree_click(self, index):
        ix = self.proxy.mapToSource(index)
        print(
            ix.data(QFileSystemModel.FilePathRole),
            ix.data(QFileSystemModel.FileNameRole),
        )


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())