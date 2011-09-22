#!/usr/bin/python2.6

# Nagios Plugin to check client puppet status
#
# Author : Camille NERON <camille.neron@gmail.com>
# Company : Carpe Hora <www.carpe-hora.com>
#
# GNU/GPL v2
#

#
# Module and variable defnition
#
from optparse import OptionParser
import sys
import MySQLdb

# Nagios return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

#
# Help and options
#

parser = OptionParser(usage="""%prog -H db_hostname -u user -p password -D db_name -n node_name 
Requirements : 

Puppet-dashboard (mysql)
Python2.6
mysqldb to python (to Debian aptitude install python-mysqldb)

Description :

Return the state of puppet client. Search the information in the puppet dashbaord database

An example of using : 

./check_dashboard_puppet.py  -H db_hostname -u user -p password -D db_name -n node_name

The plugin, will be connect to the database, and get the data with a SQL request.  """, 
                    
                    version="%prog 0.1")

parser.add_option("-H", "--hostname", dest="hostname", default="localhost",
                  help="mysql hostname \nDefault : localhost", metavar="localhost")

parser.add_option("-u", "--username", dest="username", default="dashboard",
                  help="mysql username with grant to access to dashboard puppet database", metavar="dashboard")

parser.add_option("-p", "--password", dest="password", 
                  help="mysql password", metavar="password")

parser.add_option("-D", "--database", dest="database", default="dashboard",
                  help="puppet dashboard database name", metavar="dashboard")

parser.add_option("-n", "--node_name", dest="node_name", default="puppet",
                  help="node name (puppet client)", metavar="puppet")

parser.add_option("-P", "--port", dest="port", default=3306,
                  help="mysql port\nDefault: 3306", metavar="3306")

parser.add_option("-t", "--table_name", dest="table_name", default="nodes",
                 help="table name where is stocked the status. Default: nodes", metavar="nodes")

parser.add_option("-s", "--column_status_name", dest="column_status_name", default="status",
                 help="corresponding to the column name where is the status. Default: status", metavar="status")

parser.add_option("-N", "--column_node_name", dest="column_node_name", default="name",
                 help="corresponding to the column name where is the name of the node (client). Default: name", metavar="name")

parser.add_option("-w", "--warning", dest="warning", 
                  help="warning value", metavar="changed")

parser.add_option("-c", "--critical", dest="critical", 
                  help="critical value", metavar="failed")

(options, args) = parser.parse_args()

#
# Methods
#

def mysql_connect(hostname, username, password, database, port):
  """connect to the mysql database"""
  conn = MySQLdb.connect (host = hostname,
                           user = username,
                           passwd = password,
                           db = database,
                           port = port)
  return conn

def mysql_disconnect(conn):
  """disconnect to mysql(cursor, conn)"""
  conn.close()

def value_column(report):
  """return the value column name, to the where condition of the sql request"""
  if report == "report_by_hostname":
    retour = "hostname"
  elif report == "report_by_script_name":
    retour = "script_name"
  elif report == "report_by_server_name":
    retour = "server_name"

  return retour

def get_data(column_status_name, table_name, column_node_name, node_name, conn):
  """get data in fonction of the arguments (column_status_name, table_name, column_node_name, node_name) and the connection (conn)"""
  cursor = conn.cursor()
#  where_column = value_column(report)
  try:
    cursor.execute ("SELECT %s FROM %s WHERE %s='%s'" %(column_status_name, table_name , column_node_name, node_name ))
    row = cursor.fetchone ()
    print row[0]
    return row[0]
  except:
    print "error"


def end(status, message, perfdata):
    """Exits the script with the first argument as the return code and the
       second as the message to generate output."""

    if status == OK:
        print "OK: %s | %s" % (message, perfdata)
        sys.exit(0)
    elif status == WARNING:
        print "WARNING: %s | %s" % (message, perfdata)
        sys.exit(1)
    elif status == CRITICAL:
        print "CRITICAL: %s | %s" % (message, perfdata)
        sys.exit(2)
    else:
        print "UNKNOWN: %s | %s" % (message, perfdata)
        sys.exit(3)

def validate_thresholds(warning, critical):
    """Validates warning and critical thresholds in several ways."""

#    if critical != -1 and warning == -2:
#        end(UNKNOWN, "Please also set a warning value when using warning/" +
#	             "critical thresholds!", "")
#    if critical == -1 and warning != -2:
#        end(UNKNOWN, "Please also set a critical value when using warning/" +
#	             "critical thresholds!", "")
#    if critical <= warning:
#        end(UNKNOWN, "When using thresholds the critical value has to be " +
#	              "higher than the warning value. Please adjust your " +
#		      "thresholds.", "")

def return_nagios_status(data, warning, critical, message):
  """ find the nagios status before use the end methods """
  validate_thresholds(warning, critical)
  perfdata = "time=%s" %data

  if data < warning:
    end(OK, message, perfdata)
  if data >= warning and data < critical:
    end(WARNING, message, perfdata)
  if data >= critical:
    end(CRITICAL, message, perfdata)


#
# Main
#

if __name__ == "__main__":
  conn=mysql_connect(options.hostname, 
                  options.username, 
                  options.password, 
                  options.database, 
                  options.port)

  data = get_data(options.report, options.query, options.value, conn)

  mysql_disconnect(conn)
  message = "%s:%s %s:%s" %(options.report,  options.value, options.query, data)
  return_nagios_status(float(data), float(options.warning), float(options.critical), message)
