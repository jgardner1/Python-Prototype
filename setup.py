from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='prototype',
      version=version,
      description="Javascript's Prototyping OO for Python",
      long_description="""\
The original author is Toby Ho. See
http://tobyho.com/Prototype_Inheritence_in_Python

I (Jonathan Gardner) am assuming the code is in the public domain since I
can't find any license information anywhere.

I've adapted this by making very tiny changes:
* Adding a setup script
* Modifying the attribute getter to raise an AttributeException if the
attribute is mising, instead of returning None.
* Moving doc.py to the module's doc string.
""",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: JavaScript',
      ],
      keywords='prototype javascript',
      author='Jonathan Gardner',
      author_email='jgardner@jonathangardner.net',
      url='http://tech.jonathangardner.net/wiki/Python-Prototype',
      license='Public Domain',
      py_modules=['prototype'],
      include_package_data=True,
      zip_safe=True,
      )
