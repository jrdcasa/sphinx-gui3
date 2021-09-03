'''
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
'''

from conf_base import *

# html view customizing
project = u''
copyright = u''
author = u''
version = u''
release = u'back main content list of'

# pdf style customizing
pdf_documents = [
                    ('index', u'sphinx_pdf_output', u'FIRSTPAGETITLE', u'FIRSTPAGEAUTHOR'),
                ]
pdf_use_coverpage = False # for now no cover for pdf