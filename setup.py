#from distutils.core import setup
from setuptools import setup
setup(
  name = 'py_salesforce',
  packages = ['py_salesforce'],
  package_data={
    'py_salesforce': ['py_salesforce.conf'],
  },
  version = '0.2.3',
  description = ' A Python wrapper for the Salesforce REST API and SOQL.',
  author = 'Mohamed AboElKheir',
  author_email = 'mohamed.osama.aboelkheir@gmail.com',
  url = 'https://github.com/mohamed-osama-aboelkheir/py_salesforce', 
  download_url = 'https://github.com/mohamed-osama-aboelkheir/py_salesforce/tarball/0.2.3', 
  keywords = ['salesforce', 'REST', 'API','SOQL'], 
  install_requires=['httplib2'],
  classifiers = [
    'Development Status :: 3 - Alpha',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7'],
)

