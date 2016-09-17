# py_salesforce

## Synopsis

A Python wrapper for the Salesforce REST API and SOQL. This class supports the following features:

1. Running SOQL queries.
2. Connecting to the REST API Using regular salesforce credentials, "WITHOUT" having API OAuth credentials.
3. Login and session handled automatically.
4. Supports Applying Filters to non-filterable fields (columns). e.g.: NewValue and OldValue in CaseHistory
5. Supports Child-to-Parent relations in queries.
6. Not bound by a limit for returned records.
7. Can be used to show all available SOQL Objects, and to search for specific Objects.
8. Can be used to describe an SOQL Object, and show all fields (columns), parent relations and child relations.
9. Supports exporting the output of the Query to a CSV file.

For more information about the Salesforce REST API refer to https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm

For more information about SOQL refer to https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm

## Author

Mohamed AboElKheir (mohamed.osama.aboelkheir@gmail.com)

## License

Anyone is free to copy, modify, use, or distribute this script for any purpose, and by any means. However, Please take care THIS IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND AND YOU SHOULD USE IT AT YOUR OWN RISK.

## Installation

The py_salesforce is available on pip, and can be installed as shown below:
```Bash
pip install py_salesforce
```

**NOTE:** The py_salesforce has been only tested on Python 2.7, so it is recommended to use the same version on your environment.

## Configuration

You can configure the REST and SOAP API versions you want to use in the py_salesforce.conf file.

## Authentication

This class doesn't neeed API OAuth credentails. You can use the regular salesforce credentials.

The class manages authentication, and saves the sesssion until it is expired. The script will only be prompt for your credentials if you haven't logged in before, or if the session has expired.

```python
>>> sf=py_salesforce()
Username: john.smith@example.com
Password:
<< LOGIN SUCCESS >>
```

If you wish to use the script for automation you can automate the login when the session expires by adding the "username" and the password in the py_salesforce.conf file as shown below:

```Ini
[py_salesforce]

SOAP_URL=https://login.salesforce.com/services/Soap/u/35.0
REST_URL_VER=/services/data/v35.0/

username=john.smith@example.com
password=mysecretpa$$w0rd

```

## API Reference

For detailed documentation on how to use th py_salesforce class and its fuctions you can refer to [API_reference.md](API_reference.md).

Alternatively, you can use the python help function after installing the package as showb below:

```python
>>> from py_salesforce import py_salesforce
>>> help(py_salesforce)
```

## Code Examples

1- The below example uses the "query" function to search "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"

```python
from py_salesforce import py_salesforce

sf=py_salesforce()

table="CaseHistory"
columns=["Id","CreatedDate","Field","OldValue","NewValue","Case.CaseNumber"]
conditions=['CreatedDate=THIS_MONTH',["Field=\'Owner\'","Field=\'ownerAccepted\'"]]
filters=[("NewValue","==\'John.Smith\'")]

records=sf.query(table=table,columns=columns,conditions=conditions,filters=filters)
``` 

2- The below example uses the "query_SOQL" function to perform the same task of example 1.

```python
from py_salesforce import py_salesforce

sf=py_salesforce()

soql="SELECT Id,CreatedDate,Field,OldValue,NewValue,Case.CaseNumber FROM CaseHistory WHERE CreatedDate = THIS_MONTH and (Field=\'Owner\' OR Field=\'ownerAccepted\')"                                                                                 
filters=[("NewValue","==\'John.Smith\'")]

records=sf.query_SOQL(soql=soql,filters=filters)
```

3- The below example uses the "select_all" function to select all the fields(columns) of an object.

```python
from py_salesforce import py_salesforce

sf=py_salesforce()

table="CaseHistory"
conditions=['CreatedDate=THIS_MONTH',["Field=\'Owner\'","Field=\'ownerAccepted\'"]]
filters=[("NewValue","==\'John.Smith\'")]

records=sf.select_all(table=table,conditions=conditions,filters=filters)
```

4- The below example shows how to export the records to a CSV file using the "query_to_CSV", "query_SOQL_to_CSV", and "select_all_to_CSV" functions. This should return 3 files "casehist1.csv","casehist2.csv", and"casehist3.csv" showing all non-closed cases owned by John.Smith.

```python
from py_salesforce import py_salesforce

sf=py_salesforce()

table="Case"
columns=["Id","CaseNumber","Status","Owner.Name"]
conditions=["Owner.Name=\'John.Smith\'","Status!=\'Closed\'"]
out1="casehist1.csv"

sf.query_to_CSV(table=table,columns=columns,conditions=conditions,filters=[],out=out1)


soql="SELECT Id,CaseNumber,Status,Owner.Name FROM Case WHERE Owner.Name=\'John.Smith\' and Status!=\'Closed\'"
order=["Id","CaseNumber","Status","Owner.Name"]
out2="casehist2.csv"

sf.query_SOQL_to_CSV(soql=soql,filters=[],order=order,out=out2)


table="Case"
conditions=["Owner.Name=\'John.Smith\'","Status!=\'Closed\'"]
out3="casehist3.csv"

sf.select_all_to_CSV(table=table,conditions=conditions,filters=[],order=[],out=out3)
```

5- The below shows how to search for objects (Table) having "case" in their name:

```python
>>> from py_salesforce import py_salesforce
>>> sf=py_salesforce()
>>> objects=sf.search_objects("Case")
    Case
    CaseArticle
    CaseComment
    CaseContactRole
    CaseFeed
    CaseHistory
    CaseMilestone
    ...

```

6- The below steps shows how to get a detailed describtion of an object including columns (fields), parent and child relations:

```python
>>> from py_salesforce import py_salesforce
>>> sf=py_salesforce()
>>> fields, relations = sf.describe_object("Case")
    ##########
    ## Case ##
    ##########

    ********
    Fields *
    ********
    Id        (id)
    IsDeleted         (boolean)
    CaseNumber        (string)
    ContactId         (reference)     | Parent Relation "Contact" references "Contact"
    AccountId         (reference)     | Parent Relation "Account" references "Account"
    AssetId   (reference)     | Parent Relation "Asset" references "Asset"
    EntitlementId     (reference)     | Parent Relation "Entitlement" references "Entitlement"
    ParentId          (reference)     | Parent Relation "Parent" references "Case"
    SuppliedName      (string)
    SuppliedEmail     (email)
    SuppliedPhone     (string)
    ...

    *****************
    Child relations *
    *****************
    Child Relation "ActivityHistories" references "ActivityHistory.WhatId"
    Child Relation "AttachedContentDocuments" references "AttachedContentDocument.LinkedEntityId"
    Child Relation "Attachments" references "Attachment.ParentId"
    Child Relation "Escalations__r" references "CS_CM_Escalation__c.Related_Case__c"
    Child Relation "Cases" references "Case.ParentId"
    Child Relation "CaseArticles" references "CaseArticle.CaseId"
    ...

```

