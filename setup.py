#from distutils.core import setup
from setuptools import setup
setup(
  name = 'py_salesforce',
  packages = ['py_salesforce'],
  package_data={
    'py_salesforce': ['py_salesforce.conf'],
  },
  version = '0.1',
  description = ' A Python wrapper for the Salesforce REST API and SOQL.',
  author = 'Mohamed AboElKheir',
  author_email = 'mohamed.osama.aboelkheir@gmail.com',
  url = 'https://github.com/mohamed-osama-aboelkheir/py_salesforce', 
  download_url = 'https://github.com/mohamed-osama-aboelkheir/py_salesforce/tarball/0.1', 
  keywords = ['salesforce', 'REST', 'API','SOQL'], 
  classifiers = [
    'Development Status :: 3 - Alpha',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7'],
)

