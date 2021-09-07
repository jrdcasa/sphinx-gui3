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

"""
    This class represend single markup file
"""


class Document:

    def __init__(self):
        self.file_path = None
        # ---
        self.text = None
    
    @property
    def file_name(self):
        # print(self.file_path)
        # print(os.path.basename(self.file_path))
        return os.path.basename(self.file_path) 

    def has_data(self):
        if self.file_path:
            return True
        else:
            return False
    
    # -----------------------------------------------------
    def set_new_text_content(self, text):

        # self.text = unicode(text)
        self.text = text
        
    def file_open(self, file_path):

        file = codecs.open(file_path, 'r', 'utf-8')
        self.text = file.read() 
        file.close()
        self.file_path = file_path

    def file_save(self):

        file = codecs.open(self.file_path, "wb", 'utf-8')
        file.write(self.text)
        file.close()
        self.file_open(self.file_path)

    def file_save_as(self, file_path):

        file = codecs.open(file_path, "wb", 'utf-8')
        file.write(self.text)
        file.close()
        self.file_open(file_path)
        
    def file_new(self, file_path):

        file = codecs.open(file_path, "w",  'utf-8')
        file.write('It is yours new empty markup file..')
        file.close()
        self.file_open(file_path)
        
    # -----------------------------------------------------
    def is_rst_file(self):
        if '.rst' in str(self.file_path):
            return True
        else:
            return False

    def is_md_file(self):
        if '.md' in str(self.file_path):
            return True
        else:
            return False
            
    def get_text_content(self):
        return self.text
    
    # -----------------------------------------------------
    def reset(self):
        self.__init__()
