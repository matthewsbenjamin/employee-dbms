#!/bin/bash

sqlite3 EmployeeDB.db < upload.sql

python3 main.py
