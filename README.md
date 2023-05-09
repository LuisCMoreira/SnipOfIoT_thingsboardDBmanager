# SnipOfIoT_thingsboardDBmanager

This repo. includes some python scripts to operate the standard Thingsboard hibrid DB (PostgreSQL + Cassandra).

## postgreSQLbackup.py

This script will download all database tables to CSV files.

## cassandraDBbackup.py

This script will download the keyspaces containing thingsboard timeseries data.

## cassandraDBcleaner.py

It gives the user instructions to delete specific content of the Cassandra DataBase


Note: the cassandraDB* scripts were made to run on ubuntu since these are interacting with the DB by CQLSH interface. 
