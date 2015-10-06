from distutils.core import setup
import py2exe
import glob

setup(
    console=['e-flashtemplate6.py'],
    data_files = [("animals",
                   glob.glob("animals\\*.jpg"))]
    )
