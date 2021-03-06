#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def init(api):
	api.vars['db'] = MySQLdb.connect(host= api.config['mysql']['host'],    # your host, usually localhost
	                     user= api.config['mysql']['user'],         # your username
	                     passwd= api.config['mysql']['password'],  # your password
	                     db= api.config['mysql']['database'])        # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	api.vars['cur'] = api.vars['db'].cursor()


def select(api, table, columns=['*'], by = {}):
	"""
	Select record from database
	"""

	# Building string that contains columns info and will be attached in mysql query
	string_column = ''
	for col in columns[:-1]:
		string_column += col + ','
	else:
		string_column += columns[-1]

	# Escaping columns and table strings
	column = str(MySQLdb.escape_string(string_column))
	table = str(MySQLdb.escape_string(table))

	# SQL query that will be executed
	sql = ''

	# Check if there's where conditions in SELECT
	if by:
		string_where = ''
		# Checking if key and value are the last one of 'by' dictionary
		# TODO: Check for a better way to do this verification
		dict_len = len(by)
		cont = 0

		# Building WHERE conditions to be attached in query
		for key, value in by.iteritems():
			cont += 1
			if cont < dict_len:
				string_where += key + '=' + value + ' AND '
			else:
				string_where += key + '=' + value
		where_conditions = str(MySQLdb.escape_string(string_where))
		# Creating sql query
		sql = 'SELECT %(column)s FROM %(table)s WHERE %(where)s' % dict(column=column, table=table, where=where_conditions)
	else:
		# Creating sql query
		sql = 'SELECT %(column)s FROM %(table)s ' % dict(column=column, table=table)

	# Executing sql query
	api.vars['cur'].execute(sql)

	results = []

	for row in api.vars['cur'].fetchall():
	    results += [row]

	return results

def insert(api, table, elem):
	table = str(MySQLdb.escape_string(table))
	query, params = prepareinsert(table, elem)
	api.vars['cur'].execute(query, params)
	api.vars['db'].commit()
	results = []
	for row in api.vars['cur'].fetchall():
	    results += [row]

	return results


def prepareinsert(table, mydict):
    query = """INSERT INTO {0} ({1}) VALUES ({2});"""
    d = dict(mydict)  # don't modify the input dictionary if you want to reuse it
    columns = ','.join(d.keys())
    placeholders = ','.join(['%s'] * len(d))
    values = d.values()
    return (query.format(table, columns, placeholders), values)

def close():
	db.close()