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


_url_data = {
                '1. An Introduction to reStructuredText':
                'http://docutils.sourceforge.net/docs/ref/rst/introduction.html',
                '2. A ReStructuredText Primer':
                'http://docutils.sourceforge.net/docs/user/rst/quickstart.html',
                '3. Quick reStructuredText':
                'http://docutils.sourceforge.net/docs/user/rst/quickref.html',
                '4. reStructuredText Markup Specification':
                'http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html',
                '5. Markdown Cheatsheet':
                'https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet',
                '6. Sphinx documentation contents': 'http://www.sphinx-doc.org/en/stable/contents.html',
                '7. Sphinx documentation contents': 'http://www.sphinx-doc.org/en/stable/contents.html',
                '8. Sphinx documentation contents': 'http://www.sphinx-doc.org/en/stable/contents.html',
                '9. Rst2pdf Handbook': 'http://rst2pdf.ralsina.me/handbook.html',
            }

'''
_url_data =  {
                '1. RestructuredText cheatsheet': 
                'https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst',
                '2. Sphinx and RST syntax guide': 'https://thomas-cokelaer.info/tutorials/sphinx/index.html',
                '3. Markdown Cheatsheet': 'https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet',
                '4. Sphinx documentation contents': 'http://www.sphinx-doc.org/en/stable/contents.html'
            }
'''


def get_topics():
    topic_list = _url_data.keys()
    return topic_list


def get_url_for_topic(topic):
    return _url_data[topic]

# https://www.tablesgenerator.com
