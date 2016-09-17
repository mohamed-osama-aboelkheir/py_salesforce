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
	1- Parent-to-Child relations support.
	2- Create and Edit object.

 AUTHOR: 	Mohamed Osama (mohamed.osama.aboelkheir@gmail.com)
 CREATED: 	Fri 27-Nov-2015
 LAST REVISED:	Fri 16-Sep-2016

##############
# DISCLAIMER #
##############
 Anyone is free to copy, modify, use, or distribute this script for any purpose, and by any means. However, Please take care THIS IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND AND YOU SHOULD USE IT AT YOUR OWN RISK."""

import os
import sys
import re
from xml.dom import minidom
import httplib2
import json
import ConfigParser
import getpass
import collections

try:
	import csv
except ImportError:
	pass

class py_salesforce:

	def __init__(self):

		#read config file to get urls
		self.Login_retries=3
		try:
			self.base_dir = os.path.dirname(os.path.realpath(__file__))
			self.tmp_dir = os.path.join(self.base_dir,"tmp")
			self.login_file = os.path.join(self.tmp_dir,"login.xml")
			config_file = os.path.join(self.base_dir,"py_salesforce.conf")
			config = ConfigParser.ConfigParser()
			config.read(config_file)
			options=config.options("py_salesforce")
			self.SOAP_url=config.get("py_salesforce","SOAP_URL") if "SOAP_URL".lower() in options else "https://login.salesforce.com/services/Soap/u/35.0"
			self.REST_url_ver=config.get("py_salesforce","REST_URL_VER") if "REST_URL_VER".lower() in options else "/services/data/v35.0/"
			self.username=config.get("py_salesforce","username") if "username" in options else ""
			self.password=config.get("py_salesforce","password") if "password" in options else ""
		except Exception as err:
			print "WARNING: Couldn't read config file, using default values"
			print err
			self.SOAP_url="https://login.salesforce.com/services/Soap/u/35.0"
			self.REST_url_ver="/services/data/v35.0/"
			#sys.exit(1)

		self.login()



	# (Internal usage) This function checks for session status and start new session if needed
	def login(self):
		"""(Internal usage) This function checks for session status and start new session if needed"""

		# Check for the tmp dir, if not present create it 
		if not os.path.isdir(self.tmp_dir):
			os.makedirs(self.tmp_dir)
		
		# Check if login_file exists
		if not os.path.isfile(self.login_file):
			if self.session_request():
				self.session_info()
			else:
				sys.exit(1)
		else:
			self.session_info()


	
	# (Internal usage) This function connects to salesforce to start session and save session id
	def session_request(self):
		"""(Internal usage) This function connects to salesforce to start session and saves session id"""
		
		success=False

		for i in range(int(self.Login_retries)):

			# For the first attempt try the saved username and password if present
			if i==0 and self.username and self.password:
				username=self.username
				password=self.password
			else:
				#Prompt user for credentials 
				username=raw_input("Username: ")
				password=getpass.getpass("Password: ")

			# Setup body
			body=u"""<?xml version="1.0" encoding="utf-8" ?> \
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"> \
<env:Body> \
<n1:login xmlns:n1="urn:partner.soap.sforce.com"> \
<n1:username>%s</n1:username> \
<n1:password>%s</n1:password> \
</n1:login> \
</env:Body> \
</env:Envelope>""" % (username,password)


			# Run request
			http = httplib2.Http()

			url = self.SOAP_url   
			headers = {'Content-Type': 'text/xml; charset=UTF-8' , 'SOAPAction' : 'login'}
			try:
				response, content = http.request(url, 'POST', headers=headers, body=body)
			except Exception as err:
				print "ERROR: could not connect to server"
				print err
				continue

			if response["status"] == "200": 
				open(self.login_file,"w").write(content)
				success=True
				print "<< LOGIN SUCCESS >>"
				break
			else:
				response_xml= minidom.parseString(content) 
				print ">> LOGIN FAILED!! <<"
				fault_code=response_xml.getElementsByTagName("faultcode")
				fault_string=response_xml.getElementsByTagName("faultstring")
				if len(fault_code) > 0:
					print "ERROR_CODE: "+fault_code[0].childNodes[0].data
				if len(fault_string) > 0:
					print "ERROR_STRING: "+fault_string[0].childNodes[0].data
				
				continue

		return success



	# (Internal usage) This function reads saved session information
	def session_info(self):
		"""(Internal usage) This function reads saved session information"""
		
		login_xml = minidom.parse(self.login_file)

		# Get session ID
		session_id_element=login_xml.getElementsByTagName("sessionId")
		if len(session_id_element) > 0:
			self.session_id = session_id_element[0].childNodes[0].data	
		else:
			print "ERROR: Session ID not found"
			sys.exit(1)

		# Get Server URL
		server_url_element=login_xml.getElementsByTagName("serverUrl")
		if len(server_url_element) > 0:
			pattern = re.compile('(.*://[^/]+)/.*')
			self.server_url = server_url_element[0].childNodes[0].data	
			self.server_url = pattern.search(self.server_url).group(1)
			self.REST_url = self.server_url+self.REST_url_ver 
		else:
			print "ERROR: Server URL not found"
			sys.exit(1)

		# Get User ID
		user_id_element=login_xml.getElementsByTagName("userId")
		if len(user_id_element) > 0:
			self.user_id = user_id_element[0].childNodes[0].data	

		# Get User Name
		user_name_element=login_xml.getElementsByTagName("userFullName")
		if len(user_name_element) > 0:
			self.user_name = user_name_element[0].childNodes[0].data	



	# (Internal usage) This function runs the query
	def run_query(self,url,key="records"):
		"""(Internal usage) This function runs the query"""
		
		http = httplib2.Http()
		headers = {'Authorization': 'Bearer '+self.session_id}
	
		done=False
		records=[]
		while not done:
			try:
				response, content = http.request(url, 'GET', headers=headers)
			except httplib2.MalformedHeader as err:
				if str(err)=="WWW-Authenticate":
					print ">> SESSION EXPIRED! <<"
					if self.session_request():
						self.session_info()
						headers = {'Authorization': 'Bearer '+self.session_id}
						continue	
					else:
						return False
			except Exception as err:
				print "ERROR: could not connect to server"
				print err
				return False
	
			if response["status"] == "200": 
				content_json=json.loads(content)
				records+=content_json[key]
				if "done" in content_json:
					done=content_json["done"]
				else:
					done=True

				if not done:
					url=self.server_url+content_json["nextRecordsUrl"]
				#print records
				#print(len(records))
				#print done
			else:
				print "ERROR: Query Failed"
				try:
					content_json=json.loads(content)
				except ValueError as err:
					print content
					print err
					return False
					
				if "errorCode" in content_json[0].keys():
					error_code=content_json[0]["errorCode"]
					print "ERROR_CODE: "+error_code
					if error_code=="INVALID_SESSION_ID":
						if self.session_request():
							self.session_info()
							headers = {'Authorization': 'Bearer '+self.session_id}
							continue	
						else:
							return False
				if "message" in content_json[0].keys():
					error_string=content_json[0]["message"]
					print "ERROR_STRING: "+error_string
				return False


		return records



	# This function initiates a query using REST API
	def query(self,table,columns,conditions=[],filters=[]):
		""" This function creates a query and runs it using the REST API.
ARGUMENTS:

	table: The Table (Object) of the query.
	
	columns: the list of columns (fields). This can include Child-to-Parent relations,	e.g.: Owner.Name
	
	conditions: A list of conditions to apply (with AND clause), if you wish to use OR use a list inside the list, 	e.g.: [condition1,condition2] => condition1 AND condition2, [condition3,[condition4,condition5]] => condition3 AND (condition4 OR condition5)
	
	filters: A list of conditions that will be applied AFTER the query is complete, this can be used with non filterable fields (e.g. NewValue in Casehistory). each item in the list needs to be a tuple of 2 items, first item is the column name, and the second item is a python statement that can be appied to this column.	e.g. filters=[("NewValue","==\'John.Smith\'")]

EXAMPLE:

	# The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
	sf=py_salesforce()

	table="CaseHistory"
	columns=["Id","CreatedDate","Field","OldValue","NewValue","Case.CaseNumber"]
	conditions=['CreatedDate=THIS_MONTH',["Field=\'Owner\'","Field=\'ownerAccepted\'"]]
	filters=[("NewValue","==\'John.Smith\'")]

	records=sf.query(table=table,columns=columns,conditions=conditions,filters=filters)

"""
		url = self.REST_url+"query/?q="

		# Generate query
		query="SELECT+"+",".join(columns)+"+FROM+"+table
		if conditions:
			for i in range(len(conditions)):
				if isinstance(conditions[i],list):
					conditions[i]='('+"+OR+".join(conditions[i])+')'

			query=query+"+WHERE+"+"+AND+".join(conditions)

		# Get records
		records = self.run_query(url+query)

		# If query failed don't continue
		if records is False:
			return False

		# Organise columns properly
		records=[self.flatten(record) for record in records]

		# Apply Filters
		for f in filters:
			records=eval("[ record for record in records if record[\'"+f[0]+"\'"+"] "+f[1]+"]")

		# return values
		return records


	
	def query_SOQL(self,soql,filters=[]):
		""" This function runs a query using the REST API.
ARGUMENTS:

	soql: The SOQL query.

	filters: A list of conditions that will be applied AFTER the query is complete, this can be used with non filterable fields (e.g. NewValue in Casehistory). each item in the list needs to be a tuple of 2 items, first item is the column name, and the second item is a python statement that can be appied to this column.	e.g. filters=[("NewValue","==\'John.Smith\'")]

EXAMPLE:

	# The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
	sf=py_salesforce()

	soql="SELECT Id,CreatedDate,Field,OldValue,NewValue,Case.CaseNumber FROM CaseHistory WHERE CreatedDate = THIS_MONTH and (Field=\'Owner\' OR Field=\'ownerAccepted\')"	
	filters=[("NewValue","==\'John.Smith\'")]

	records2=sf.query_SOQL(soql=soql,filters=filters)

"""

		url = self.REST_url+"query/?q="

		# Generate query
		query=soql.replace(" ","+")

		# Get records
		records = self.run_query(url+query)

		# If query failed don't continue
		if records is False:
			return False

		# Organise columns properly
		records=[self.flatten(record) for record in records]

		# Apply Filters
		for f in filters:
			records=eval("[ record for record in records if record[\'"+f[0]+"\'"+"] "+f[1]+"]")

		# return values
		return records



	# Put records in CSV
	def to_CSV(self,records,out="out.csv",order=[]):
		"""This function exports records returned from query or query_SOQL into a CSV File 
ARGUMENTS:

	records: List of dictionaries, returned from query or query_SOQL
	
	out: the name and path of the output file
	
	order: a list having the order in which the columns should be displayed (can only contain columns included in the used records)
"""

		# If the CSV module is not found print error and exit
		if "csv" not in sys.modules:
			print "ERROR: csv module not found .. unable to create CSV file" 
			return None

		# Check if any records were returned
		if not records:
			print "No records were found .. ignoring CSV file creation"
			return None

		# check if columns in order are valid and correct case if needed
		if order:
			for i in range(len(order)):
				if not records[0].keys().count(order[i]):
					for k in records[0].keys():
						if re.match(order[i],k,re.IGNORECASE):
							order[i]=k
							break

		keys=order if order else records[0].keys()
		enc_keys=[dict(zip(keys,[k.encode('utf8') for k in keys]))]

		# encode Unicode
		enc_records=[]
		for record in records:
			enc_record={}
			for key in keys:
				enc_record[key]=record[key].encode('utf8') if isinstance(record[key],unicode) else record[key]
			enc_records.append(enc_record)
				
				

		with open(out, 'w') as output_file:
			dict_writer = csv.DictWriter(output_file, keys,quoting=csv.QUOTE_ALL)
			dict_writer.writerows(enc_keys)
			dict_writer.writerows(enc_records)


	# This function runs the query and puts the output in a CSV file
	def query_to_CSV(self,table,columns,conditions=[],filters=[],out="out.csv"):
		""" This function creates a query and runs it using the REST API, then exports the output to a CSV file.
ARGUMENTS:

	table,columns,conditions,filters: Same as the query() function.

	out:  the name and path of the output file.

EXAMPLE:

    # The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
    sf=py_salesforce()

    table="CaseHistory"
    columns=["Id","CreatedDate","Field","OldValue","NewValue","Case.CaseNumber"]
    conditions=['CreatedDate=THIS_MONTH',["Field=\'Owner\'","Field=\'ownerAccepted\'"]]
    filters=[("NewValue","==\'John.Smith\'")]
	out="casehist.csv"

	sf.query_to_CSV(table=table,columns=columns,conditions=conditions,filters=filters,out=out)

"""


		records=self.query(table,columns,conditions,filters)

		self.to_CSV(records,out,columns)	



	# This function runs the query with SOQL and puts the output in a CSV file
	def query_SOQL_to_CSV(self,soql,filters=[],order=[],out="out.csv"):
		""" This function runs a query using the REST API, and exports the output to a CSV file.
ARGUMENTS:

    soql: The SOQL query.

    filters: same as the query and query_SOQL functions.

	order: a list having the order in which the columns should be displayed (can only contain columns included in the used records)
 
	out: the name and path of the output file.
 
EXAMPLE:

    # The below example searches "CaseHistory" for items created This month and the changed field was "Owner" OR "OwnerAccepted", then applied a filter on the NewValue to only be "John.Smith"
    sf=py_salesforce()

    soql="SELECT Id,CreatedDate,Field,OldValue,NewValue,Case.CaseNumber FROM CaseHistory WHERE CreatedDate = THIS_MONTH and (Field=\'Owner\' OR Field=\'ownerAccepted\')"
    filters=[("NewValue","==\'John.Smith\'")]
	order=["Id","CreatedDate","Field","OldValue","NewValue","Case.CaseNumber"]
	out="casehist.csv"

	sf.query_SOQL_to_CSV(soql=soql,filters=filters,order=order,out=out)

"""

		records=self.query_SOQL(soql,filters)
				
		self.to_CSV(records,out,order)	



	# This is a function used to flatten nested dicts to create a list
	def flatten(self, d, parent_key='', sep='.'):
		""" (Internal Usage) This is a function used to flatten nested dicts to create a list """
		items = []
		for k, v in d.items():
			if k=='attributes' and type(v) is dict:
				continue
			new_key = parent_key + sep + k if parent_key else k
			if isinstance(v, collections.MutableMapping):
				items.extend(self.flatten(v, new_key, sep=sep).items())
			else:
				items.append((new_key, v))
		return dict(items)

		

	# This function shows all available objects for your environment
	def show_all_objects(self,print_all=True):
		""" This function shows all available objects for your environment.
ARGUMENTS:

	print_all: If True, the names of the Objects will be printed on the screen, otherwise a list of objects will only be returned.

"""

		url = self.REST_url+"sobjects"

		# Get objects
		objects = self.run_query(url=url,key="sobjects")

		# If query failed don't continue
		if objects is False:
			return False

		if print_all:
			for obj in objects:
				if obj["queryable"]:
					print obj["name"]
				else:
					print obj["name"]+" ... (DOESN'T SUPPORT QUERY)" 

		return objects



	# This function searches Objects with a certain string in their name
	def search_objects(self,string,print_all=True,case_sensitive=False):
		""" This function searches for Objects.
ARGUMENTS:

	string: The string to search for in the Object name.

    print_all: If True, the names of the Objects will be printed on the screen, otherwise a list of objects will only be returned.

	case_sensitive: If True, case will be matched.

EXAMPLE:

	>>> objects=sf.search_objects("Case")
	Case
	CaseArticle
	CaseComment
	CaseContactRole
	CaseFeed
	CaseHistory
	CaseMilestone
	...
	
	
"""


		all_objects=self.show_all_objects(print_all=False)

		if case_sensitive:
			objects=[ obj for obj in all_objects if string in obj["name"] ]
		else:
			objects=[ obj for obj in all_objects if string.lower() in obj["name"].lower() ]

		if print_all:
			for obj in objects:
				if obj["queryable"]:
					print obj["name"]
				else:
					print obj["name"]+" ... (DOESN'T SUPPORT QUERY)" 

		return objects



	# This functions describes the fields and the relations of an object
	def describe_object(self,object_name,print_fields=True,print_child_rel=True):
		"""This functions describes the fields and the relations of an object.
ARGUMENTS:

	object_name: Name of the Object(Table)

	print_fields: If True, the names of the fields (columns) will be printed on the screen, otherwise a list of fields will only be returned.

	print_child_rel: If True, the names of the child relations will be printed on the screen, otherwise a list of Child relations will only be returned.

EXAMPLES:

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
	
	
"""

		url = self.REST_url+"sobjects/"+object_name+"/describe"

		# Get objects
		fields = self.run_query(url=url,key="fields")
		child_relations= self.run_query(url=url,key="childRelationships")

		# If query failed don't continue
		if fields is False or child_relations is False :
			return False

		# Get longest name to justify
		#longest_field=len(max([field["name"]+field["type"] for field in fields],key=len))+4
		

		if print_fields or print_child_rel:
			print "###"+"#"*len(object_name)+"###"
			print "## "+object_name+" ##"
			print "###"+"#"*len(object_name)+"###"
			print ""
		if print_fields:
			print "********"
			print "Fields *"
			print "********"
			for field in fields:
				filterable="\t  | CAN'T BE USED IN WHERE CLAUSE" if not field["filterable"] else ""
				relation="\t  | Parent Relation \""+field["relationshipName"]+"\" references \""+"\" OR \"".join(field["referenceTo"])+"\"" if field["referenceTo"] and field["relationshipName"] is not None else ""
				
				#print field["name"]+"  ("+field["type"]+")"+" "*(longest_field-len(field["name"]+field["type"]))+filterable+relation
				print field["name"]+"\t  ("+field["type"]+")"+filterable+relation

		if print_child_rel and child_relations:
			print ""
			print "*****************"
			print "Child relations *"
			print "*****************"
			for relation in child_relations:
				if relation["relationshipName"] is not None:
					print "Child Relation \""+relation["relationshipName"]+"\" references \""+relation["childSObject"]+"."+relation["field"]+"\"" 

		return fields , child_relations



	# fucntion to select all columns (fields) from an Object
	def select_all(self,table,conditions=[],filters=[]):
		""" This function generates a query that shows all possible columns of an Object
ARGUMENTS:

	table, conditions, filters: same as query() functions.

"""
		
		columns=[field["name"] for field in self.describe_object(table,print_fields=False,print_child_rel=False)[0]]	
		records=self.query(table=table,columns=columns,conditions=conditions,filters=filters)
		
		return records
	


	# fucntion to select all columns (fields) from an Object to a CSV file
	def select_all_to_CSV(self,table,conditions=[],filters=[],order=[],out="out.csv"):
		""" This function generates a query that shows all possible columns of an Object and exports the output to a CSV file
ARGUMENTS:

	table, conditions, filters: same as query() functions.

	order: a list having the order in which the columns should be displayed (can only contain columns included in the used records)

	out: the name and path of the output file 

"""
		records=self.select_all(table=table,conditions=conditions,filters=filters)
		self.to_CSV(records,out,order)	
		
