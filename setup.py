from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='imageHide',
      version=version,
      description="Encrypt and show encrypted images",
      long_description="",
      classifiers=[],
      keywords='',
      author='Jeffrey Ness',
      author_email='jeffrey.ness@rackspace.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['PIL', 'pycrypto'],
      test_suite='nose.collector',
      entry_points= {'console_scripts': ['imageHide = imageHide.main:main']},
      )
