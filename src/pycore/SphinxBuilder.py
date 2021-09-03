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

import sys
import platform
import os
import tempfile
import subprocess
import shutil

import src.pycore.app_utils as app_utils

PYTHON_BIN_PATH = os.path.dirname(sys.executable)
if platform.system() == 'Windows':
    sphinxbuild_path = os.path.join(PYTHON_BIN_PATH, 'Scripts', 'sphinx-build')
else:
    sphinxbuild_path = os.path.join(PYTHON_BIN_PATH, 'sphinx-build')


class SphinxBuilder:
    def __init__(self):

        self.tmp_html_dir = self.__get_tempdir('tebeHTML')
        self.tmp_pdf_dir = self.__get_tempdir('tebePDF')
        # ---
        self.Content = None
        # ---
        self.theme = None
        self.theme_template_dir = app_utils.abspath('pycore/sphinx_conf_template')
        # ---
        self.confdir = None
        # ----
        self.where_pdf_saved = None
        # ----
        self.__html_is_builded_for = None
        # ---
        self.set_theme()

    @staticmethod
    def __get_tempdir(prefix_string):

        dirpath = tempfile.mkdtemp()
        dirname = os.path.basename(dirpath)
        new_dirname = prefix_string + '_' + dirname
        new_dirpath = dirpath.replace(dirname, new_dirname)
        os.rename(dirpath, new_dirpath)
        return new_dirpath

    # -----------------------------------------------------
    def assign_content_object(self, content_object):
        self.Content = content_object

    def get_available_themes(self):
        theme_list = []
        for name in os.listdir(self.theme_template_dir):
            if '.' not in name:
                theme_list.append(name)
                theme_list.sort()
        return theme_list

    def set_theme(self, theme='basic_like_paper'):
        # ---
        self.confdir = self.theme_template_dir
        self.confdir = os.path.join(self.confdir, theme)
        # ---
        self.theme = theme

    # -----------------------------------------------------

    @property
    def source_dir_path(self):
        if self.Content:
            return self.Content.source_dir_path
        else:
            return None

    # -----------------------------------------------------

    '''
    def _build(self, buildername='html'):
        if self.Content.conf_file_path:
            confdir = self.source_dir_path
        else:
            confdir = self.confdir
        #---
        if buildername == 'html':
            outdir = self.tmp_html_dir
            doctreedir = self.tmp_html_dir
        if buildername == 'pdf':
            outdir = self.tmp_pdf_dir
            doctreedir = self.tmp_pdf_dir
        #---
        sphinx_app = Sphinx(    srcdir = self.source_dir_path, 
                                confdir = confdir,
                                outdir = outdir, 
                                doctreedir = self.tmp_html_dir, 
                                buildername = buildername   )
        #---
        sphinx_app.build()  

    def build_html(self):
        if self.source_dir_path:
            self._build('html')
            print 'build_html done'

    def build_pdf(self):
        if self.source_dir_path:
            self._build('pdf')
            print 'build_pdf done'
    '''

    def build_html(self):
        if self.source_dir_path:
            # ---
            scrdir = self.source_dir_path
            outdir = self.tmp_html_dir
            # ---
            if self.Content.conf_file_path:
                proc = subprocess.Popen([sphinxbuild_path,
                                         '-b', 'html',
                                         scrdir, outdir])
            else:
                proc = subprocess.Popen([sphinxbuild_path,
                                         '-b', 'html',
                                         '-c', self.confdir,
                                         scrdir, outdir])
            proc.wait()
            # ---
            self.__html_is_builded_for = self.source_dir_path
            print('build_html done')

    def build_pdf(self, dst_file=None):
        self.where_pdf_saved = None
        # ---
        for fname in os.listdir(self.tmp_pdf_dir):
            if '.pdf' in fname:
                file_pth = os.path.join(self.tmp_pdf_dir, fname)
                os.remove(file_pth)
        # ---
        if self.source_dir_path:
            # ---
            scrdir = self.source_dir_path
            print(scrdir)
            outdir = self.tmp_pdf_dir
            # ---
            if self.Content.conf_file_path:
                proc = subprocess.Popen([sphinxbuild_path,
                                         '-b', 'pdf',
                                         scrdir, outdir])
            else:
                proc = subprocess.Popen([sphinxbuild_path,
                                         '-b', 'pdf',
                                         '-c', self.confdir,
                                         scrdir, outdir])
            proc.wait()
            # ---
            for fname in os.listdir(self.tmp_pdf_dir):
                if '.pdf' in fname:
                    scr_file = os.path.join(self.tmp_pdf_dir, fname)
                    if not dst_file:
                        dst_file = os.path.join(self.source_dir_path, fname)
                    shutil.copyfile(scr_file, dst_file)
            # ---
            self.where_pdf_saved = dst_file
        print('build_pdf done')

    # -----------------------------------------------------
    def is_html_builded(self):
        if self.source_dir_path:
            if self.source_dir_path == self.__html_is_builded_for:
                return True
            else:
                return False
        else:
            return False

    def html_path_for(self, markup_file):
        html_file_name = markup_file
        html_file_name = html_file_name.replace('.rst', '.html')
        html_file_name = html_file_name.replace('.md', '.html')
        html_file_path = os.path.join(self.tmp_html_dir, html_file_name)
        return html_file_path

    # -----------------------------------------------------
    def delete_tmpdirs(self):
        shutil.rmtree(self.tmp_html_dir)
        shutil.rmtree(self.tmp_pdf_dir)

    def close(self):
        self.delete_tmpdirs()
        self.tmp_html_dir = None
        self.tmp_pdf_dir = None

    def __del__(self):
        if self.tmp_html_dir:
            self.close()
