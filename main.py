#!/usr/bin/python3

# REPL Link
# https://repl.it/@bm441/ThunderousStupendousDesignmethod

import sqlite3
import re

# DB Operations handles all database CRUD operations, including validation
#   and deduplication
class DBOperations:
  sql_create_table_firsttime = "CREATE TABLE IF NOT EXISTS EmployeeUoB (" \
    "EmployeeID INT NOT NULL PRIMARY KEY, " \
    "title VARCHAR(12) NOT NULL, " \
    "forename VARCHAR(255) NOT NULL, " \
    "surname VARCHAR(255) NOT NULL, " \
    "email VARCHAR(255) NOT NULL, " \
    "salary INT NOT NULL );"

  sql_create_table = "CREATE TABLE IF NOT EXISTS EmployeeUoB (" \
    "EmployeeID INT NOT NULL PRIMARY KEY, " \
    "title VARCHAR(12) NOT NULL, " \
    "forename VARCHAR(255) NOT NULL, " \
    "surname VARCHAR(255) NOT NULL, " \
    "email VARCHAR(255) NOT NULL, " \
    "salary INT NOT NULL );"

  sql_insert = "INSERT INTO EmployeeUoB (EmployeeID, title, forename, surname, email, salary) VALUES ({}, '{}', '{}', '{}', '{}', {});"
  sql_select_all = "SELECT * FROM EmployeeUoB;"
  sql_search = "SELECT * FROM EmployeeUoB WHERE EmployeeID = {};"
  sql_delete_data = "DELETE FROM EmployeeUoB WHERE EmployeeID = {};"
  sql_drop_table = "DROP TABLE EmployeeUoB;"
 
  # Constructor will connect to the database and create the employee table if it doesn't exist
  def __init__(self):
    try:
      self.conn = sqlite3.connect("EmployeeDB.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table_firsttime)
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("EmployeeDB.db")
    self.cur = self.conn.cursor()

  def create_table(self):
    try:
      self.get_connection()

      # Query the db master table and return if it already exists
      self.cur.execute("SELECT name FROM sqlite_master WHERE name = 'EmployeeUoB';")
      results = self.cur.fetchall()

      # If not table 'EmployeeUoB' exists, then tell the user and return
      # without executing the create table script
      if results.__len__() != 0:
        print("Table already exists")
        return

      self.cur.execute(self.sql_create_table)
      self.conn.commit()
      print("Table created successfully")
      return
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()

      emp = Employee()
      # Validation loop will only break when the function - func - is happy with the input
      def validationLoop(message, failMsg, func):
        data = input(message)
        while not func(data):
          print("Must be a" + failMsg)
          data = input("Please try again - " + message)

      # Prevent user from duplicating an employee ID
      results = True
      while results:
        validationLoop("Enter Employee ID: ", "n Integer", emp.set_employee_id)
        self.cur.execute(self.sql_search.format(str(emp.get_employee_id())))
        results = self.cur.fetchone()
        if results:
          print('Employee Already Exists')

      validationLoop("Enter Employee Title: ", " string only", emp.set_employee_title)
      validationLoop("Enter Employee First Name: ", " string only", emp.set_forename)
      validationLoop("Enter Employee Surname: ", " string only", emp.set_surname)
      validationLoop("Enter Employee Email: ", " valid email", emp.set_email)
      validationLoop("Enter Employee Salary: ", " number, or currency value", emp.set_salary)

      # Insert the validated data into the database
      stmt = self.sql_insert.format(emp.get_employee_id(), emp.get_employee_title(), emp.get_forename(), emp.get_surname(), emp.get_email(), emp.get_salary())
      self.cur.execute(stmt)
      self.conn.commit()

      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      results = self.cur.fetchall()
      
      # Instantiate a table and render it to the screen
      Table(results).render()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
  def search_data(self):
    try:
      self.get_connection()
      employeeID = int(input("Enter Employee ID: "))
      self.cur.execute(self.sql_search.format(str(employeeID)))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Employee ID: " + str(detail))
          elif index == 1:
            print("Employee Title: " + detail)
          elif index == 2:
            print("Employee Name: " + detail)
          elif index == 3:
            print("Employee Surname: " + detail)
          elif index == 4:
            print("Employee Email: " + detail)
          else:
            print("Salary: "+ str(detail))
      else:
        print ("No Record")
            
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def update_data(self):

    # Returns a string of the format 'col = val, ' to be added to the update statement
    def build_set_column(col, val):
      if type(val) == type('str'):
        if len(val) > 0:
          return "{} = '{}', ".format(col, val)
        return ''
        
      if val > 1:
          return "{} = '{}', ".format(col, val)

      return ''

    def build_update_stmt(e):
      id = e.get_employee_id()
      title = e.get_employee_title()
      fname = e.get_forename()
      sname = e.get_surname()
      email = e.get_email()
      salary = e.get_salary()

      stmt = "UPDATE EmployeeUob SET "
      stmt += build_set_column("title", title)
      stmt += build_set_column("forename", fname)
      stmt += build_set_column("surname", sname)
      stmt += build_set_column("email", email)
      stmt += build_set_column("salary", salary)

      stmt += "WHERE EmployeeID = {};".format(str(id))
      stmt = re.sub(",\s+WHERE", " WHERE", stmt)
      return stmt

    # Validation loop will ensure that the new data is accepted by the user class
    #   according to it's regex matcher
    def updateValidationLoop(message, failMsg, func):
      data = input(message)
      if len(data) == 0:
        return
      while not func(data):
        print("Must be a" + failMsg)
        data = input("Please try again - " + message)
        return

    try:
      self.get_connection()
      emp = Employee()

      # Based on the employee ID - check if they exist - if not - return to menu
      # User cannot update UID
      updateValidationLoop("Enter Employee ID: ", "n Integer", emp.set_employee_id)
      self.cur.execute(self.sql_search.format(str(emp.get_employee_id())))
      results = self.cur.fetchone()
      if not results:
        print('Employee Does Not Exist')
        return

      print("Update values - leave blank to not update")
      updateValidationLoop("\tEnter Employee Title: ", " string only", emp.set_employee_title)
      updateValidationLoop("\tEnter Employee First Name: ", " string only", emp.set_forename)
      updateValidationLoop("\tEnter Employee Surname: ", " string only", emp.set_surname)
      updateValidationLoop("\tEnter Employee Email: ", " valid email", emp.set_email)
      updateValidationLoop("\tEnter Employee Salary: ", " number, or currency value", emp.set_salary)

      # Build an update statement & execute
      stmt = build_update_stmt(emp)
      result = self.cur.execute(stmt)
      self.conn.commit()
      if result.rowcount != 0:
        print (str(result.rowcount)+ "Row(s) affected.")
      else:
        print ("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def delete_data(self):
    try:
      self.get_connection()

      # ask for an employee ID
      #   No need to validate, if ID doesn't exist then we don't need to worry
      #   about deleting something that doesn't exist
      employeeID = int(input("Enter Employee ID: "))
      stmt = self.sql_delete_data.format(str(employeeID))
      result = self.cur.execute(stmt)
      if result.rowcount != 0:
        self.conn.commit()
        print (str(result.rowcount)+ " Row(s) affected.")
      else:
        print ("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally: 
      self.conn.close()

  def self_destruct(self):
    # it's an oop joke ... self ... geddit?
    # NOT exposed on the menu
    try:
      self.get_connection()
      self.cur.execute(self.sql_drop_table)
      self.conn.commit()
      print("Table deleted")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

    
class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  # Will only match an ID 0-999
  def set_employee_id(self, id):
    exp = r"(^[0-9]{0,3}$)"
    if re.match(exp, id):
      self.employeeID = int(id)
      return True
    
    return False

  # Will only accept a string followed by 0 or 1 '.'
  def set_employee_title(self, title):
    exp = r"(^[A-z]+\.?$)"
    if re.match(exp, title):
      self.empTitle = title
      return True
    
    return False

  # Will only accept a string
  def set_forename(self, forename):
    exp = r"(^[A-z]+$)"
    if re.match(exp, forename):
      self.forename = forename
      return True
    
    return False
  
  # Will only accept a string
  def set_surname(self,surname):
    exp = r"(^[A-z]+$)"
    if re.match(exp, surname):
      self.surname = surname
      return True
    
    return False

  # Will only accept a valid email
  def set_email(self, email):
    # NOTE - This regular expression is not my work
    # taken from emailregex.com
    exp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(exp, email):
      self.email = email
      return True
    
      return False
  
  # Will only accept an integer value
  def set_salary(self,salary):
    exp = r"(^[0-9]+$)"
    if re.match(exp, salary):
      self.salary = int(salary)
      return True
    
    return False
  
  def get_employee_id(self):
    return self.employeeID

  def get_employee_title(self):
    return self.empTitle
  
  def get_forename(self):
    return self.forename
  
  def get_surname(self):
    return self.surname
  
  def get_email(self):
    return self.email
  
  def get_salary(self):
    return self.salary

  def __str__(self):
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)

class Table() :
  def __init__(self, r):
    self.results = r
    self.tbl = ''

  def render(self):
    pad = 2
    ws = (' ' * pad)
    tbl = '\nQuery Results:\n'
    tbl += u'\u250F'
    headerTuple = ("Id", "Title", "First Name     ", "Surname      ", "Email                      ", "Salary    ")
    headerIter = iter(headerTuple)
    for i in headerIter:
      tbl += u'\u2501' * (len(ws)) # whitespace
      tbl += u'\u2501' * (len(i)) # matching the header
      tbl += u'\u2501' * (len(ws)) # whitespace
      tbl += u'\u2533' # ┓
    tbl += u'\u2513\n'
    tbl = re.sub(u'\u2533\u2513', u'\u2513', tbl)

    headerIter = iter(headerTuple)
    for i in headerIter:
      tbl += u'\u2503' + ws + i + ws
    tbl += u'\u2503\n'

    def spacer():
      output = u'\u2523'
      headerIter = iter(headerTuple)
      for i in headerIter:
        output += u'\u2501' * (len(ws)) # whitespace
        output += u'\u2501' * (len(i)) # matching the header
        output += u'\u2501' * (len(ws)) # whitespace
        output += u'\u254b' # ┓
      output += u'\u252B\n'
      output = re.sub(u'\u254b\u252B', u'\u252B', output)
      return output

      # add in results
    for i in range(len(self.results)):
      tbl += spacer()
      for ii in range(6):
        s = str(self.results[i][ii])
        tbl += u'\u2503' + ws + s + ' ' * (len(headerTuple[ii]) - len(str(s))) + ws 
      tbl += u'\u2503\n'

    # end row
    headerIter = iter(headerTuple)
    tbl += u'\u2517'
    for i in headerIter:
      tbl += u'\u2501' * (len(ws)) # whitespace
      tbl += u'\u2501' * (len(i)) # matching the header
      tbl += u'\u2501' * (len(ws)) # whitespace
      tbl += u'\u253B' # ┓
    tbl += u'\u251B\n'
    tbl = re.sub(u'\u253B\u251B', u'\u251B', tbl)
      
    print(tbl)


# The main function will parse arguments. 
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
class Main:

  def run(self):
    while True:
      print("\n Menu:")
      print("**********")
      print("\t1. Create table EmployeeUoB")
      print("\t2. Insert data into EmployeeUoB")
      print("\t3. Select all data into EmployeeUoB")
      print("\t4. Search an employee")
      print("\t5. Update data some records")
      print("\t6. Delete data some records")
      print("\t7. Exit\n")

      __choose_menu = int(input("Enter your choice: "))
      db_ops = DBOperations()
      if __choose_menu == 1:
        db_ops.create_table()
      elif __choose_menu == 2:
        db_ops.insert_data()
      elif __choose_menu == 3:
        db_ops.select_all()
      elif __choose_menu == 4:
        db_ops.search_data()
      elif __choose_menu == 5:
        db_ops.update_data()
      elif __choose_menu == 6:
        db_ops.delete_data()
      elif __choose_menu == 7:
        exit(0)
      elif __choose_menu == 999:
        db_ops.self_destruct()
      else:
        print ("Invalid Choice")


if __name__ == '__main__':
  program = Main()
  program.run()