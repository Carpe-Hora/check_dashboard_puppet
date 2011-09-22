check_dashboard_puppet.py
===============

Licence
-------

This plugin is writted by Carpe-Hora <www.carpe-hora.com> Camille Neron <camille_neron@gmail.com>.

Of course, check_dashboard_puppet is under GNU GPL v2 : http://www.gnu.org/licenses/gpl-2.0.html

Requirements
------------

* Puppet-dashboard (mysql)
* Python2.6
* mysqldb to python (to Debian aptitude install python-mysqldb)

Description
-----------

Return the state of puppet client. Search the information in the puppet dashbaord database

An example of using : 

./check_dashboard_puppet.py  -H db_hostname -u user -p password -D db_name -n node_name

The plugin, will be connect to the database, and get the data with a SQL request. 

TODO List
----------
