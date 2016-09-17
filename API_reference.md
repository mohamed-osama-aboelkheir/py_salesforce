# py_salesforce API Reference

```python
class py_salesforce
 |  Methods defined here:
 |  
 |  __init__(self)
 |  
 |  describe_object(self, object_name, print_fields=True, print_child_rel=True)
 |      This functions describes the fields and the relations of an object ... returns 2 Lists of dictionaries (fields and child relations) if successful and returns False if failed.
 |      ARGUMENTS:
 |      
 |              object_name: Name of the Object(Table)
 |      
 |              print_fields: If True, the names of the fields (columns) will be printed on the screen, otherwise a list of fields will only be returned.
 |      
 |              print_child_rel: If True, the names of the child relations will be printed on the screen, otherwise a list of Child relations will only be returned.
 |      
 |      EXAMPLES:
 |      
 |              >>> fields, relations = sf.describe_object("Case")
 |              ##########
 |              ## Case ##
 |              ##########
 |              
 |              ********
 |              Fields *
 |              ********
 |              Id        (id)
 |              IsDeleted         (boolean)
 |              CaseNumber        (string)
 |              ContactId         (reference)     | Parent Relation "Contact" references "Contact"
 |              AccountId         (reference)     | Parent Relation "Account" references "Account"
 |              AssetId   (reference)     | Parent Relation "Asset" references "Asset"
 |              EntitlementId     (reference)     | Parent Relation "Entitlement" references "Entitlement"
 |              ParentId          (reference)     | Parent Relation "Parent" references "Case"
 |              SuppliedName      (string)
 |              SuppliedEmail     (email)
 |              SuppliedPhone     (string)
 |              ...
 |              
 |              *****************
 |              Child relations *
 |              *****************
 |              Child Relation "ActivityHistories" references "ActivityHistory.WhatId"
 |              Child Relation "AttachedContentDocuments" references "AttachedContentDocument.LinkedEntityId"
 |              Child Relation "Attachments" references "Attachment.ParentId"
 |              Child Relation "Escalations__r" references "CS_CM_Escalation__c.Related_Case__c"
 |              Child Relation "Cases" references "Case.ParentId"
 |              Child Relation "CaseArticles" references "CaseArticle.CaseId"
 |              ...
 |  
 |  flatten(self, d, parent_key='', sep='.')
 |      (Internal Usage) This is a function used to flatten nested dicts to create a list
 |  
 |  login(self)
 |      (Internal usage) This function checks for session status and start new session if needed
 |  
 |  query(self, table, columns, conditions=[], filters=[])
 |      This function creates a query and runs it using the REST API ... returns List of dictionaries (records) if successful and returns False if failed.
 |      ARGUMENTS:
 |      
 |              table: The Table (Object) of the query.
 |              
 |              columns: the list of columns (fields). This can include Child-to-Parent relations,      e.g.: Owner.Name
 |              
 |              conditions: A list of conditions to apply (with AND clause), if you wish to use OR use a list inside the list,  e.g.: [condition1,condition2] => condition1 AND condition2, [condition3,[condition4,condition5]] => condition3 AND (condition4 OR condition5)
 |              
 |              filters: A list of conditions that will be applied AFTER the query is complete, this can be used with non filterable fields (e.g. NewValue in Casehistory). each item in the list needs to be a tuple of 2 items, first item is the column name, and the second item is a python statement that can be appied to this column.   e.g. filters=[("NewValue","=='John.Smith'")]
 |      
 |      EXAMPLE:
 |      
 |              # The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
 |              sf=py_salesforce()
 |      
 |              table="CaseHistory"
 |              columns=["Id","CreatedDate","Field","OldValue","NewValue","Case.CaseNumber"]
 |              conditions=['CreatedDate=THIS_MONTH',["Field='Owner'","Field='ownerAccepted'"]]
 |              filters=[("NewValue","=='John.Smith'")]
 |      
 |              records=sf.query(table=table,columns=columns,conditions=conditions,filters=filters)
 |  
 |  query_SOQL(self, soql, filters=[])
 |      This function runs a query using the REST API ... returns List of dictionaries (records) if successful and returns False if failed.
 |      ARGUMENTS:
 |      
 |              soql: The SOQL query.
 |      
 |              filters: A list of conditions that will be applied AFTER the query is complete, this can be used with non filterable fields (e.g. NewValue in Casehistory). each item in the list needs to be a tuple of 2 items, first item is the column name, and the second item is a python statement that can be appied to this column.   e.g. filters=[("NewValue","=='John.Smith'")]
 |      
 |      EXAMPLE:
 |      
 |              # The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
 |              sf=py_salesforce()
 |      
 |              soql="SELECT Id,CreatedDate,Field,OldValue,NewValue,Case.CaseNumber FROM CaseHistory WHERE CreatedDate = THIS_MONTH and (Field='Owner' OR Field='ownerAccepted')"       
 |              filters=[("NewValue","=='John.Smith'")]
 |      
 |              records2=sf.query_SOQL(soql=soql,filters=filters)
 |  
 |  query_SOQL_to_CSV(self, soql, filters=[], order=[], out='out.csv')
 |      This function runs a query using the REST API, and exports the output to a CSV file.
 |      ARGUMENTS:
 |      
 |          soql: The SOQL query.
 |      
 |          filters: same as the query and query_SOQL functions.
 |      
 |              order: a list having the order in which the columns should be displayed (can only contain columns included in the used records)
 |       
 |              out: the name and path of the output file.
 |       
 |      EXAMPLE:
 |      
 |          # The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
 |          sf=py_salesforce()
 |      
 |          soql="SELECT Id,CreatedDate,Field,OldValue,NewValue,Case.CaseNumber FROM CaseHistory WHERE CreatedDate = THIS_MONTH and (Field='Owner' OR Field='ownerAccepted')"
 |          filters=[("NewValue","=='John.Smith'")]
 |              order=["Id","CreatedDate","Field","OldValue","NewValue","Case.CaseNumber"]
 |              out="casehist.csv"
 |      
 |              sf.query_SOQL_to_CSV(soql=soql,filters=filters,order=order,out=out)
 |  
 |  query_to_CSV(self, table, columns, conditions=[], filters=[], out='out.csv')
 |      This function creates a query and runs it using the REST API, then exports the output to a CSV file.
 |      ARGUMENTS:
 |      
 |              table,columns,conditions,filters: Same as the query() function.
 |      
 |              out:  the name and path of the output file.
 |      
 |      EXAMPLE:
 |      
 |          # The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
 |          sf=py_salesforce()
 |      
 |          table="CaseHistory"
 |          columns=["Id","CreatedDate","Field","OldValue","NewValue","Case.CaseNumber"]
 |          conditions=['CreatedDate=THIS_MONTH',["Field='Owner'","Field='ownerAccepted'"]]
 |          filters=[("NewValue","=='John.Smith'")]
 |              out="casehist.csv"
 |      
 |              sf.query_to_CSV(table=table,columns=columns,conditions=conditions,filters=filters,out=out)
 |  
 |  run_query(self, url, key='records')
 |      (Internal usage) This function runs the query ... returns List of dictionaries (records) if successful and returns False if failed
 |  
 |  search_objects(self, string, print_all=True, case_sensitive=False)
 |      This function searches for Objects ... returns List of dictionaries (objects) if successful and returns False if failed.
 |      ARGUMENTS:
 |      
 |              string: The string to search for in the Object name.
 |      
 |          print_all: If True, the names of the Objects will be printed on the screen, otherwise a list of objects will only be returned.
 |      
 |              case_sensitive: If True, case will be matched.
 |      
 |      EXAMPLE:
 |      
 |              >>> objects=sf.search_objects("Case")
 |              Case
 |              CaseArticle
 |              CaseComment
 |              CaseContactRole
 |              CaseFeed
 |              CaseHistory
 |              CaseMilestone
 |              ...
 |  
 |  select_all(self, table, conditions=[], filters=[])
 |      This function generates a query that shows all possible columns of an Object ... returns List of dictionaries (records) if successful and returns False if failed.
 |      ARGUMENTS:
 |      
 |              table, conditions, filters: same as query() functions.
 |  
 |  select_all_to_CSV(self, table, conditions=[], filters=[], order=[], out='out.csv')
 |      This function generates a query that shows all possible columns of an Object and exports the output to a CSV file
 |      ARGUMENTS:
 |      
 |              table, conditions, filters: same as query() functions.
 |      
 |              order: a list having the order in which the columns should be displayed (can only contain columns included in the used records)
 |      
 |              out: the name and path of the output file
 |  
 |  session_info(self)
 |      (Internal usage) This function reads saved session information
 |  
 |  session_request(self)
 |      (Internal usage) This function connects to salesforce to start session and saves session id ... returns boolean
 |  
 |  show_all_objects(self, print_all=True)
 |      This function shows all available objects for your environment ... returns List of dictionaries (objects) if successful and returns False if failed.
 |      ARGUMENTS:
 |      
 |              print_all: If True, the names of the Objects will be printed on the screen, otherwise a list of objects will only be returned.
 |  
 |  to_CSV(self, records, out='out.csv', order=[])
 |      This function exports records returned from query or query_SOQL into a CSV File 
 |      ARGUMENTS:
 |      
 |              records: List of dictionaries, returned from query or query_SOQL
 |              
 |              out: the name and path of the output file
 |              
 |              order: a list having the order in which the columns should be displayed (can only contain columns included in the used records)

```
