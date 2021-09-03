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
import codecs

from src.pycore.create_index_content import create_index_content


class Content:
    def __init__(self):
        # ----
        self.source_dir_path = None
        self.tree = None

    @property
    def project_name(self):
        return os.path.basename(self.source_dir_path)

    def set_source_dir(self, source_dir_path):
        self.source_dir_path = source_dir_path
        if self.tree:
            self.tree.reload()

    @property
    def conf_file_path(self):
        if self.source_dir_path:
            supposed_index_file = os.path.join(self.source_dir_path, 'conf.py')
            is_this_file_exist = os.path.isfile(supposed_index_file)
            if is_this_file_exist:
                return os.path.join(self.source_dir_path, 'index.rst')
            else:
                return None
        else:
            return None

    @property
    def index_file_path(self):
        if self.source_dir_path:
            supposed_index_file = os.path.join(self.source_dir_path, 'index.rst')
            is_this_file_exist = os.path.isfile(supposed_index_file)
            if is_this_file_exist:
                return os.path.join(self.source_dir_path, 'index.rst')
            else:
                return None
        else:
            return None

    def is_ready_to_build(self):
        if self.source_dir_path:
            return True
        else:
            return False

    def get_markup_filenames_list(self):
        markup_file_list = []
        for name in os.listdir(self.source_dir_path):
            if ('.md' in name) or ('.rst' in name):
                if name != 'index.rst':
                    name = name.replace('.md', '')
                    name = name.replace('.rst', '')
                    markup_file_list.append(name)
                    markup_file_list.sort()
        return markup_file_list

    def create_index_file(self):
        index_file_content = create_index_content(self.get_markup_filenames_list())
        index_file_path = os.path.join(self.source_dir_path, 'index.rst')
        file = codecs.open(index_file_path, "w",  'utf-8')
        file.write(index_file_content)
        file.close()
