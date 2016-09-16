from distutils.core import setup
setup(
  name = 'py_salesforce',
  packages = ['py_salesforce'],
  version = '0.1',
  description = ' A Python wrapper for the Salesforce REST API and SOQL. This class supports the following features:\n
            1- Running SOQL queries.\n
            2- Connecting to the REST API Using regular salesforce credentials, "WITHOUT" having API OAuth credentials.\n
            3- Login and session handled automatically.\n
            4- Supports Applying Filters to non-filterable fields (columns). e.g.: NewValue and OldValue in CaseHistory\n
            5- Supports Child-to-Parent relations in queries.\n
            6- Not bound by a limit for returned records.\n
            7- Can be used to show all available SOQL Objects, and to search for specific Objects.\n
            8- Can be used to describe an SOQL Object, and show all fields (columns), parent relations and child relations.\n
            9- Supports exporting the output of the Query to a CSV file.\n
\n
            For more information about the Salesforce REST API refer to https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm\n
            For more information about SOQL refer to https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm',
  author = 'Mohamed AboElKheir',
  author_email = 'mohamed.osama.aboelkheir@gmail.com',
  url = 'https://github.com/mohamed-osama-aboelkheir/py_salesforce', 
  download_url = 'https://github.com/mohamed-osama-aboelkheir/py_salesforce/tarball/0.1', 
  keywords = ['salesforce', 'REST', 'API','SOQL'], 
  classifiers = [],
)

