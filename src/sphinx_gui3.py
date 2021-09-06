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
# """

import sys
import os
import time

from PyQt5 import QtWidgets, QtGui, QtCore, QtPrintSupport

from src.gui.Editor import Editor
from src.gui.Preview import Preview
from src.gui.Tree import Tree

from src.pycore.Environment import Content, Document, SphinxBuilder, Rst2PdfBuilder
from src.pycore.markup_utils import rst_to_html, md_to_html, is_markup_file
from src.pycore.app_utils import abspath, APP_PATH
import src.pycore.help_content as help_content

from src.info import appdata


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # ---
        self.Tree = Tree()
        self.Tree.assign_content(Content)
        self.Editor = Editor()
        self.Editor.assign_document(Document)
        # ---
        self.tab_widget = QtWidgets.QTabWidget()
        self.CurrentFilePreview = Preview()
        self.SphinxCurentFilePreview = Preview()
        self.SphinxIndexFilePreview = Preview()
        self.HelpPage = Preview()
        # ---
        self.tab_widget.addTab(self.CurrentFilePreview, "current file preview")
        self.tab_widget.addTab(self.SphinxCurentFilePreview, "sphinx current file preview")
        self.tab_widget.addTab(self.SphinxIndexFilePreview, "sphinx index file preview")
        self.tab_widget.addTab(self.HelpPage, "help")
        # ---
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(splitter)
        splitter.addWidget(self.Tree)
        splitter.addWidget(self.Editor)
        splitter.addWidget(self.tab_widget)
        # ---
        self.setupActions()
        self.connectSignals()
        # ---
        self.createMenus()
        self.createToolBars()
        self.showMaximized()
        # ---
        self.set_apptitle()
        self.status = self.statusBar()
        self.setWindowIcon(QtGui.QIcon("icons/logo.png"))
        # ---
        self.scrolls_data = {}
        # ---
        self.printer = QtPrintSupport.QPrinter()
        
    def setupActions(self):
        self.openAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/open_file.png")), "Open file", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("It opens markup file")
        self.openAction.triggered.connect(self.openFile)

        self.openFolderAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/open_folder.png")), "Open Folder", self)
        self.openFolderAction.setShortcut("Ctrl+Shift+O")
        self.openFolderAction.setStatusTip("It opens folder with markup files")
        self.openFolderAction.triggered.connect(self.openFolder)        

        self.saveAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/save.png")), "Save File", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setStatusTip("It saves current file")
        self.saveAction.triggered.connect(self.saveFile)  
        
        self.saveAsAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/save_as.png")), "Save File As", self)
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.setStatusTip("It saves current file with new name")
        self.saveAsAction.triggered.connect(self.saveFileAs)

        self.autoSaveAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/auto.png")), "Auto save", self, checkable=True)
        self.autoSaveAction.setStatusTip("If pushed file will always be saved before closing")   

        self.newAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/new.png")), "New File", self)
        self.newAction.setShortcut("Ctrl+Shift+N")
        self.newAction.setStatusTip("It craetes new empty markup file")
        self.newAction.triggered.connect(self.newFile)

        self.quitAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/quit.png")), "Quit", self)
        self.quitAction.setShortcut("Ctrl+QCtrl+Q")
        self.quitAction.setStatusTip("Quit")
        self.quitAction.triggered.connect(self.close) 
 
        self.buildHTMLAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/build.png")), "Sphinx build", self)
        self.buildHTMLAction.setStatusTip("It builds sphinx project as html and display it on right side")
        self.buildHTMLAction.triggered.connect(self.buildHTML)

        self.sphinx_buildPDFAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/pdf_sphinx.png")),
                                                       "Sphinx PDF build", self)
        self.sphinx_buildPDFAction.setStatusTip("It builds sphinx project as PDF and saves it")
        self.sphinx_buildPDFAction.triggered.connect(self.buildPDF)

        self.sphinx_createIndexFile = QtWidgets.QAction(QtGui.QIcon(abspath("icons/index.png")),
                                                        "Create index file", self)
        self.sphinx_createIndexFile.setStatusTip("It create or update index.rst file needed for sphinx build")
        self.sphinx_createIndexFile.triggered.connect(self.create_index_file)

        self.sphinx_theme = QtWidgets.QAction(QtGui.QIcon(abspath("icons/theme.png")), "Select sphinx theme", self)
        self.sphinx_theme.setStatusTip("It lets you choose theme for sphinx view")
        self.sphinx_theme.triggered.connect(self.custom_theme)

        self.this_buildPDFAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/pdf_this.png")),
                                                     "Current file to PDF", self)
        self.this_buildPDFAction.setStatusTip("It creates PDF for current file and save it")
        self.this_buildPDFAction.triggered.connect(self.build_this_PDF) 

        self.printAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/print.png")),
                                             "Print current file preview", self)
        self.printAction.setStatusTip("It prints current file preview on system printer")
        self.printAction.triggered.connect(self.directPrint)
        
        self.PreviewRefreshAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/refresh_preview.png")),
                                                      "Refresh current file preview", self)
        self.PreviewRefreshAction.setShortcut("Ctrl+R")
        self.PreviewRefreshAction.setStatusTip("Refresh current file preview")
        self.PreviewRefreshAction.triggered.connect(self.live_update)

        self.synchronizeScrollsSwitch = QtWidgets.QAction(QtGui.QIcon(abspath("icons/scroll.png")),
                                                          "Synchronize scrolls", self, checkable=True)
        self.synchronizeScrollsSwitch.setStatusTip("If pushed editor and live preview scrolls will be synchronized") 
    
        self.autoPreviewRefreshAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/auto.png")),
                                                          "Current file preview auto refresh", self, checkable=True)
        self.autoPreviewRefreshAction.setStatusTip("If pushed preview will auto updated when content change") 
        self.autoPreviewRefreshAction.setChecked(True) 

        self.aboutAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/about.png")), "Info", self)
        self.aboutAction.setStatusTip("It shows app info")
        self.aboutAction.triggered.connect(self.about)
        
        self.helpAction = QtWidgets.QAction(QtGui.QIcon(abspath("icons/help.png")), "Learn about..", self)
        self.helpAction.setStatusTip("It shows information about the selected topic")
        self.helpAction.triggered.connect(self.help)

    def connectSignals(self):
        self.Editor.textChanged.connect(self.auto_live_update)
        self.Editor.verticalScrollBar().valueChanged.connect(self.scrolls_synchronize)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.openFolderAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)
        # ---
        self.this_buildMenu = self.menuBar().addMenu("Markup file")
        self.this_buildMenu.addAction(self.PreviewRefreshAction)
        self.this_buildMenu.addAction(self.this_buildPDFAction)
        self.this_buildMenu.addAction(self.printAction)
        # ---
        self.buildMenu = self.menuBar().addMenu("Sphinx project")
        self.buildMenu.addAction(self.buildHTMLAction)
        self.buildMenu.addAction(self.sphinx_theme)
        self.buildMenu.addAction(self.sphinx_createIndexFile)
        self.buildMenu.addSeparator()
        self.buildMenu.addAction(self.sphinx_buildPDFAction)
        # ---
        self.this_helpMenu = self.menuBar().addMenu("Help")
        self.this_helpMenu.addAction(self.aboutAction)
        self.this_helpMenu.addAction(self.helpAction)
        
    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.openFolderAction)
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.saveAction)
        self.fileToolBar.addAction(self.autoSaveAction)
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.newAction)
        #--
        self.thisbuildToolBar = self.addToolBar("Markup file")
        self.thisbuildToolBar.addAction(self.printAction)
        self.thisbuildToolBar.addAction(self.this_buildPDFAction)
        self.thisbuildToolBar.addSeparator()
        self.thisbuildToolBar.addAction(self.PreviewRefreshAction)
        self.thisbuildToolBar.addAction(self.autoPreviewRefreshAction)
        self.thisbuildToolBar.addSeparator()
        self.thisbuildToolBar.addAction(self.synchronizeScrollsSwitch)
        #--
        self.sphinxbuildToolBar = self.addToolBar("Sphinx project")
        self.sphinxbuildToolBar.addAction(self.buildHTMLAction)
        self.sphinxbuildToolBar.addAction(self.sphinx_theme)
        self.sphinxbuildToolBar.addAction(self.sphinx_createIndexFile)
        self.sphinxbuildToolBar.addSeparator()
        self.sphinxbuildToolBar.addAction(self.sphinx_buildPDFAction)
        #--
        self.helpToolBar = self.addToolBar("Help")
        self.helpToolBar.addAction(self.aboutAction)
        self.helpToolBar.addAction(self.helpAction)

    # ---------------------------------
    def openFile(self, file_path=None, is_from_new_project=True):
        self.autosave()
        # ---
        self.scrolls_archive_positions()
        # ---
        directory = Content.source_dir_path
        if not directory : directory = APP_PATH
        if not file_path:
            file_path = QtWidgets.QFileDialog.getOpenFileName(  caption = 'Open markup file',
                                                            directory = directory,
                                                            filter = "Markup File (*.rst *.md)")[0]
        print(file_path)
        # ---
        if file_path and is_markup_file(file_path):    
            file_path = str(file_path)
            # ---
            Document.file_open(file_path)
            if is_from_new_project:
                Content.set_source_dir(os.path.dirname(file_path))
            # ---
            self.reload_data()

    def openFolder(self):
        self.autosave()
        # ---
        self.scrolls_archive_positions()
        # ---
        directory = Content.source_dir_path
        if not directory : directory = APP_PATH       
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(  self,
                                                            directory = directory,
                                                            caption = 'Open folder')
        # ---
        if dir_path:
            Content.set_source_dir(dir_path)
            Document.reset()
            if Content.index_file_path:
                Document.file_open(Content.index_file_path)
            self.reload_data()

    def saveFile(self):
        if Document.has_data():
            text_in_editor = self.Editor.toPlainText()
            Document.set_new_text_content(text_in_editor)
            try:
                Document.file_save()
                self.showStatusInfo('saved to [%s] file' %Document.file_name)
            except IOError:
                self.showStatusInfo("unable to save to [%s] file" %Document.file_name)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        # ---
        directory = Document.file_path.replace(Document.file_name, 'Copy_of_' + Document.file_name)
        if not directory : directory = ''
        file_path = QtWidgets.QFileDialog.getSaveFileName(  caption = 'Save markup file as',
                                                        directory = directory,
                                                        filter = "Markup File (*.rst *.md)")[0]
        # ---
        if file_path:
            text_in_editor = self.Editor.toPlainText()
            Document.set_new_text_content(text_in_editor)
            # ---
            try:
                Document.file_save_as(file_path)
                if Content.source_dir_path in file_path:
                    self.openFile(file_path, is_from_new_project=False)
                else:
                    self.openFile(file_path, is_from_new_project=True)
                self.showStatusInfo('saved as [%s] file' %Document.file_name)
            except IOError:
                self.showStatusInfo("unable to save as [%s] file" %Document.file_name)
            
    def newFile(self):
        self.autosave()
        # ---
        directory = Content.source_dir_path
        if not directory :
            directory = ''
        directory = os.path.join(directory, 'new.rst')
        file_path = QtWidgets.QFileDialog.getSaveFileName(  caption = 'New markup file',
                                                        directory = directory,
                                                        filter = "Markup File (*.rst *.md)")[0]
        if file_path:
            file_path = str(file_path)
            Document.file_new(file_path)
            # --
            autosave_status = self.autoSaveAction.isChecked()
            window.autoSaveAction.setChecked(False)  #  autosave hold
            self.openFile(file_path)
            window.autoSaveAction.setChecked(autosave_status)  # autosave back to previous
            # --
            self.showStatusInfo('new [%s] file created ' % Document.file_name)

    def autosave(self):
        if self.autoSaveAction.isChecked():
            if Document.has_data:
                self.saveFile()
                self.showStatusInfo("autosaved to [%s] file" % Document.file_name)

    # ---------------------------------

    def reload_data(self):
        self.Editor.load_document()
        self.reload_sphinx_previews()
        # ---
        self.live_update()
        # ---
        window.scrols_load_position_from_archive()
        # ---
        self.set_apptitle()

    def reload_sphinx_previews(self):
        if SphinxBuilder.is_html_builded():
            # self.SphinxCurentFilePreview.scroll_fix()
            index_html_path = SphinxBuilder.html_path_for('index.html')
            self.SphinxIndexFilePreview.show_html(index_html_path)
            # ---
            this_file_html_path = SphinxBuilder.html_path_for(Document.file_name)
            self.SphinxCurentFilePreview.show_html(this_file_html_path)
        else:
            self.SphinxIndexFilePreview.setHtml('(html not built yet)')
            self.SphinxCurentFilePreview.setHtml('(html not built yet)')

    def live_update(self):
        markup_text = self.Editor.get_text_content()
        markup_text = u'%s'%markup_text
        # ---
        # indow.CurrentFilePreview.scroll_fix()
        # ---
        if not Document.file_path:  # if there is no document loaded on app start - default render as markdown
            html = rst_to_html(markup_text)
            self.showStatusInfo('rst content rendered')
        elif Document.is_rst_file():  # if restructured text file loaded
            html = rst_to_html(markup_text)
            self.showStatusInfo('rst content rendered')
        elif Document.is_md_file():  # if markdown text file loaded
            html = md_to_html(markup_text) 
            self.showStatusInfo('md content rendered')
        else:  # in other cases any render
            html = ''
            self.showStatusInfo('non markup file opened')
        # ---
        if Content.source_dir_path:
            LocalFile = os.path.join(Content.source_dir_path, '') # it create feake file path
        else:
            LocalFile = ''
        self.CurrentFilePreview.setHtml(html, QtCore.QUrl.fromLocalFile(LocalFile))
    
    def auto_live_update(self):
        if window.autoPreviewRefreshAction.isChecked():
            self.live_update()
            self.Editor.setFocus()

    # ---------------------------------
    def buildHTML(self):
        if not Content.index_file_path:
            self.create_index_file()
        if Content.is_ready_to_build():
            self._cursor_wait(True)
            SphinxBuilder.build_html()
            self._cursor_wait(False)
            # ---
            self.reload_sphinx_previews()
            if self.tab_widget.currentIndex() == 0:
                self.tab_widget.setCurrentIndex(1)
        else:
            QtWidgets.QMessageBox.information(None, 'Info', 'No data to sphinx build - try to open some sphinx content')

    def buildPDF(self):
        if not Content.index_file_path:
            self.create_index_file()
        if Content.is_ready_to_build():
            # ---asking pdf filename
            init_filename = Content.project_name + '.pdf'
            init_directory = os.path.join(Content.source_dir_path, init_filename)
            file_path = QtWidgets.QFileDialog.getSaveFileName(  caption = 'New pdf file',
                                                                directory = init_directory,
                                                                filter = "Pdf file (*.pdf)")[0]
            # ---
            if not file_path == '':
                self._cursor_wait(True)
                SphinxBuilder.build_pdf(file_path)
                self._cursor_wait(False)
        else:
            QtWidgets.QMessageBox.information(None, 'Info', 'No data to sphinx build - try to open some sphinx content')        

    
    def build_this_PDF(self):
        if Document.is_rst_file():
            # ---asking pdf filename
            init_directory = Document.file_path.replace('.rst', '.pdf')
            pdf_file_path = QtWidgets.QFileDialog.getSaveFileName(  caption = 'New pdf file',
                                                                    directory = init_directory,
                                                                    filter = "Pdf file (*.pdf)")[0]
            # pdf_file_path = str(pdf_file_path)
            # ---
            if not pdf_file_path == '':
                self._cursor_wait(True)
                Rst2PdfBuilder.build_pdf_from_rst_file(Document.file_path, pdf_file_path)
                self._cursor_wait(False)
        else:
            QtWidgets.QMessageBox.information(None, 'Info', 'This option available only for rst file')
            
    def create_index_file(self):
        if Content.index_file_path:
            reply = QtWidgets.QMessageBox.question(None, "Index file already exist!",
                                                   'Index file already exist for current Sphinx project. '
                                                   'Do you want replace it?',
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                Content.create_index_file()
                self.showStatusInfo('Index file updated')
        else :
            reply = QtWidgets.QMessageBox.question(None, "Index file will be created!",
                                                   'There is no index file in current Sphinx project '
                                                   'an it will be created now.',
                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
            if reply == QtWidgets.QMessageBox.Ok:
                Content.create_index_file()
                self.showStatusInfo('Index file created')

    def custom_theme(self):
        # ---Asking dialog
        available_theme_list = SphinxBuilder.get_available_themes()
        current_theme_index = available_theme_list.index(SphinxBuilder.theme)
        theme_selected = QtWidgets.QInputDialog.getItem(None, 'Sphinx theme', 'Select theme for sphinx build',
                                                        available_theme_list, current_theme_index , False)[0]
        theme_selected = str(theme_selected)
        # ---Seting selected theme
        SphinxBuilder.set_theme(theme_selected)
        # ---Info if conf.py already in current sphinx content
        if Content.conf_file_path:
            QtWidgets.QMessageBox.information(None, 'Info', 'Please not that you already have theme defined '
                                                            'by conf.py file in your project folder. Tebe build in '
                                                            'theme will be not used!')
        # ---Sphinx rebuilt
        if SphinxBuilder.is_html_builded():
            self.buildHTML()
        
    # ---------------------------------
    def directPrint(self):
        dlg = QtPrintSupport.QPrintDialog(self.printer)
        if dlg.exec_():
            self.showStatusInfo('Printing ...')
            self.CurrentFilePreview.page().print(self.printer, self.print_completed)

    def print_completed(self, success):
        if success:
            self.showStatusInfo('... printed')
        else:
            self.showStatusInfo('Print error')

    # ---------------------------------
    def about(self):
        window.HelpPage.show_url('https://tebe.readthedocs.io/en/latest/')
        self.tab_widget.setCurrentIndex(3)
        # ---
        QtWidgets.QMessageBox.information(None, 'Info', appdata._about)
                
    def help(self):
        # ---Asking dialog
        available_topics = help_content.get_topics()
        topic_selected = QtWidgets.QInputDialog.getItem(None, 'Help content',
                                                        'Select topic', available_topics, 0 , False)[0]
        topic_selected = str(topic_selected)
        # ---Showing help page
        window.HelpPage.show_url(help_content.get_url_for_topic(topic_selected))
        # ---
        self.tab_widget.setCurrentIndex(3)
        
    def _cursor_wait(self, wait=False):
        if wait:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        else:
            QtWidgets.QApplication.restoreOverrideCursor()
            
    def set_apptitle(self):
        apptitle = appdata._appname + ' ' + appdata._version + ' - sphinx writer '
        if Document.file_path:
            apptitle += ' - [%s] in [%s]'%(Document.file_name, Content.project_name)
        self.setWindowTitle(apptitle)

    def showStatusInfo(self, massage=''):
        current_time_string = time.strftime("%H:%M:%S", time.gmtime())
        massage = 'at %s - %s'%(current_time_string, massage)
        self.status.showMessage(massage)
    
    def closeEvent(self, event):
        SphinxBuilder.close()
        event.accept()

    def scrolls_archive_positions(self):
        scroll_editor = self.Editor.verticalScrollBar().value()
        scroll_CurrentFilePreview = window.CurrentFilePreview.scroll_get_position()
        scroll_SphinxCurentFilePreview = window.SphinxCurentFilePreview.scroll_get_position()
        # ---
        self.scrolls_data[Document.file_path] = [scroll_editor, scroll_CurrentFilePreview,
                                                 scroll_SphinxCurentFilePreview]

    def scrols_load_position_from_archive(self):
        if Document.file_path in window.scrolls_data:
            scroll_editor = window.scrolls_data[Document.file_path][0]
            self.Editor.verticalScrollBar().setValue(scroll_editor)
            # ---
            scroll_CurrentFilePreview = window.scrolls_data[Document.file_path][1]
            self.CurrentFilePreview.scroll_to_absposition(scroll_CurrentFilePreview)
            # ---
            scroll_SphinxCurentFilePreview = window.scrolls_data[Document.file_path][2]
            self.SphinxCurentFilePreview.scroll_to_absposition(scroll_SphinxCurentFilePreview)
        else:
            window.Editor.verticalScrollBar().setValue(0)
            window.CurrentFilePreview.scroll_up()
            window.SphinxCurentFilePreview.scroll_up()

    def scrolls_synchronize(self):
        pass
        if window.synchronizeScrollsSwitch.isChecked():
            self.CurrentFilePreview.scroll_to_relposition(window.Editor.get_scroll_relposition())
            self.SphinxCurentFilePreview.scroll_to_relposition(window.Editor.get_scroll_relposition())


def Main():

    global app, window
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # ---
    window.CurrentFilePreview.setHtml('<h4><< Try to write some rest content</h3>')
    sys.exit(app.exec_())


if __name__ == "__main__":
    Main()

