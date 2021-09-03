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

```


Changelog
---------
The **sphinx-gui3** (aka Tebe) 0.2.3 (J. Ramos)

- Improve installation (J. Ramos).
- Some changes along the py files to fulfill with PEP8
- Use CLI to run the program.
- Change the name Tebe to sphinx-gui3.

Tebe 0.2.2

- port to python3 and PyQt5, python 2 dropped

Tebe 0.1

- first public release (beta stage) with all main features implemented


Requirements
------------
1. Python 3
#. pyqt5
#. pyqtwebengine 
#. sphinx
#. rst2pdf
#. docutils
#. recommonmark
#. mistune

How to install
--------------
Tebe is available through PyPI and can be install with pip command by typing::

   pip install tebe

Please note that the requirements listed above must be installed separately.

To run tebe run the ``Tebe.py`` file from the installed package directory.

Licence
-------
Tebe is free software;
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

Code repository (sphinx-gui3): https://github.com/jrdcasa/sphinx-gui3.git

Contact: Javier Ramos <jrdcasa@gmail.com>


