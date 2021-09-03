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

from src.pycore.Content import Content as _Content
from src.pycore.Document import Document as _Document
from src.pycore.SphinxBuilder import SphinxBuilder as _SphinxBuilder
from src.pycore.Rst2PdfBuilder import Rst2PdfBuilder as _Rst2PdfBuilder

Content = _Content()
Document = _Document()
SphinxBuilder = _SphinxBuilder()
Rst2PdfBuilder = _Rst2PdfBuilder()

SphinxBuilder.assign_content_object(Content)
