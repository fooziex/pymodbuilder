pymodbuilder
============

Python module build script. 

Usage:
-----------
Currently you should edit the "home" variable to be an extant directory, and comment out any modules you don't want built. You need a working Python build environment on your PATH, including git, hg, and svn. 
Warning! this script deletes directories with abandon (well, it wants to). Make sure you have nothing important in any dir inside the "home" you specify.

To do:
------
- Convert "modules" dict to SQLite db
- Command line options: module package types, modules to build, add modules to database (seperate script?)
- Use cwd / command line option for home directory
- Support Linux
- More output, robustness
- Automatic diff on modules, e.g. pycares
- Build branches / release versions
- Build Numpy / Scipy with ICL
- Make it 'pythonic'
