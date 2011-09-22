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
  """disconnect to mysql(conn)"""
  conn.close()

def get_data(column_status_name, table_name, column_node_name, node_name, conn):
  """get data in fonction of the arguments (column_status_name, table_name, column_node_name, node_name) and the connection (conn)"""
  cursor = conn.cursor()
  try:
    cursor.execute ("SELECT %s FROM %s WHERE %s='%s'" %(column_status_name, table_name , column_node_name, node_name ))
    row = cursor.fetchone ()
    return row[0]
  except:
    print "[ERROR] : Thanks to check if the node is available, and if the connexion information is valid."


def end(status, message):
    """Exits the script with the first argument as the return code and the
       second as the message to generate output."""

    if status == "unchanged":
        print "OK: %s" % (message)
        sys.exit(0)
    elif status == "changed":
        print "WARNING: %s" % (message)
        sys.exit(1)
    elif status == "failed":
        print "CRITICAL: %s" % (message)
        sys.exit(2)
    else:
        print "UNKNOWN: %s" % (message)
        sys.exit(3)

#
# Main
#

if __name__ == "__main__":
  conn=mysql_connect(options.hostname, 
                  options.username, 
                  options.password, 
                  options.database, 
                  options.port)


  data = get_data(options.column_status_name, options.table_name, options.column_node_name, options.node_name, conn)
  mysql_disconnect(conn)
  message = "%s %s" %(options.node_name, data)
  end(data, message)
