sphinx-gui3 - sphinx writer
============================
The sphinx-gui3 (aka Tebe) is a simple but powerful editor for Markdown and reStructuredText markup languages
with Sphinx and Rst2Pdf power included.
It can be used as a text editor for creating articles or even books.
You can also use it to work with any sphinx docs you have for yours project.
The mission of the project is to provide a simple and practical tool that will interest non-programer people
to use markup syntax and sphinx for any text document writing.

The original Tebe package can be found in https://bitbucket.org/lukaszlaba/tebe/src/master/ (author: Lukasz Laba)

I decided to make some minor changes to adapt the project to my needs.

How to install
--------------

The changes in the package makes the installation even easier:
   
```bash
# Create a virtual environment
cd <dir>
python3 -m venv sandbox_sphinxgui3
# Activate the venv
source sandbox_sphinxgui3/bin/activate
# Clone the github
git clone https://github.com/jrdcasa/sphinx-gui3.git
cd sphinx-gui3/
python setup.py install
# After this you can run the program as:
sphinx-gui3 
# Once the program has been installed, in oder to run it in any terminal
# you need to activate the python envioronment and run the previous command
# In this example:
source <path_to_the_venv>/sandbox_sphinxgui3/bin/activate
sphinx-gui3 
```


Changelog
---------
The **sphinx-gui3** (aka Tebe) 0.2.3 (J. Ramos)

- Improve installation (J. Ramos).
- Some changes along the py files to fulfill with PEP8
- Use CLI to run the program.
- Change the name Tebe to sphinx-gui3.
- Add sphinx_rtd_theme
- Allow the edition of python files to manually configure config.py
- Correct error in the function create_index_file in Content.py. The application closed with errors with no index.rst file is loaded.
- Correct error in the function saveFileAs in sphinx_gui3.py. The application closed with errors with noo files loaded in the Tree.
- New folder in toolbar and menus
- Add contextual menu to the Tree window
- Relative can be used for rst files. In the previous version if the rst file is in a different directory to the index.rst file, the Sphinx view is not generated.

Tebe 0.2.2

- port to python3 and PyQt5, python 2 dropped

Tebe 0.1

- first public release (beta stage) with all main features implemented


Requirements
------------

1. Python 3
1. pyqt5
1. pyqtwebengine 
1. sphinx
1. rst2pdf
1. docutils
1. recommonmark
1. mistune
1. mock
1. sphinx_rtd_theme


Licence
-------
Sphinx-gui3 (aka Tebe) is free software;
you can redistribute it and/or modify it under the terms of the **GNU General Public License**
as published by the Free Software Foundation;
either version 2 of the License,
or (at your option) any later version.

Copyright (C) 2017-2020 Lukasz Laba <lukaszlaba@gmail.com>


Contributions
-------------
If you want to help out, create a pull request or write email.

More information
----------------
Project original website: https://tebe.readthedocs.io

Code original repository: https://bitbucket.org/lukaszlaba/tebe

PyPI package: https://pypi.python.org/pypi/tebe

Contact: Lukasz Laba <lukaszlaba@gmail.com>

More information on sphinx-gui3
-------------------------------

Code repository (sphinx-gui3): https://github.com/jrdcasa/sphinx-gui3.git

Contact: Javier Ramos <jrdcasa@gmail.com>


