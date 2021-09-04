"""
 This is a dummy setup.py to use
    pyhton setup.py build
    python setup.py install

 Configuration is given in pyproject.toml and setup.cfg
"""
from setuptools import setup
import sys
import subprocess


# Install packages from pip ==============================================================
def install_with_pip(pack, vers=None):

    # sys.executable gives the path to the python interpreter
    if vers is None:
        print("** sphinx-gui3: Installing {}".format(pack))
        subprocess.call([sys.executable, "-m", "pip", "install", "{0}".format(pack)])
    else:
        print("** sphinx-gui3: Installing {}=={}".format(pack, vers))
        subprocess.call([sys.executable, "-m", "pip", "install", "{0}=={1}".format(pack, vers)])


if __name__ == "__main__":
 


    print(sys.path)

    # Install requirements ===================================
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    for ipack in required:
        try:
            pkg, version = ipack.split(">=")[0:2]
            if pkg[0] == "#": continue
            install_with_pip(pkg, version)
        except ValueError:
            pkg = ipack
            if pkg[0] == "#": continue
            install_with_pip(pkg)

    setup()
