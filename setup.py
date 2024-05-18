"""Setup for PynHTM which wraps libtinyhtm in python."""

import subprocess

import numpy
from Cython.Build import cythonize
from setuptools import Extension, setup

proc = subprocess.Popen("make", stderr=subprocess.STDOUT, shell=True)
output, stderr = proc.communicate(input)
status = proc.wait()
if status:
    raise Exception("failed to *make* libtinyhtm")

pynyHTM_extension = Extension(
    name="PynyHTM",
    sources=["pynyhtm.pyx"],
    libraries=[":libtinyhtm.a"],
    library_dirs=["."],
    include_dirs=[numpy.get_include()],
    language="c++",
    py_limited_api=True,
)

setup(name="PynyHTM", ext_modules=cythonize([pynyHTM_extension]))
