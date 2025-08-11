from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("Context_menu.py"))
setup(ext_modules=cythonize("file_copy_util.py"))