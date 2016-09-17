#! /usr/bin/env python
""" A Python wrapper for the Salesforce REST API and SOQL. This class supports the following features:
    1- Running SOQL queries.
    2- Connecting to the REST API Using regular salesforce credentials, "WITHOUT" having API OAuth credentials.
    3- Login and session handled automatically.
    4- Supports Applying Filters to non-filterable fields (columns). e.g.: NewValue and OldValue in CaseHistory
    5- Supports Child-to-Parent relations in queries.
    6- Not bound by a limit for returned records.
    7- Can be used to show all available SOQL Objects, and to search for specific Objects.
    8- Can be used to describe an SOQL Object, and show all fields (columns), parent relations and child relations.
    9- Supports exporting the output of the Query to a CSV file.

    For more information about the Salesforce REST API refer to https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm
    For more information about SOQL refer to https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm


    TODO:
    1- Parent-to-Child relations support.                                                                                                                 2- Create and Edit object.

 AUTHOR:    Mohamed Osama (mohamed.osama.aboelkheir@gmail.com)
 CREATED:   Fri 27-Nov-2015
 LAST REVISED:  Fri 17-Sep-2016

##############
# DISCLAIMER #
##############
 Anyone is free to copy, modify, use, or distribute this script for any purpose, and by any means. However, Please take care THIS IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND AND YOU SHOULD USE IT AT YOUR OWN RISK."""



from py_salesforce import py_salesforce
