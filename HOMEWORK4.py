import sqlite3
from tkinter import *

class table:

    def __init__(self, tbl_name):
        self._name = tbl_name

        self._conn = sqlite3.connect("database.db")
        print('Opened database successfully. ')
        self.c = self._conn.cursor()
        self.c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='{}'; ".format(self._name))
        if len(self.c.fetchall()) > 0:
            # Delete table
            self.c.execute("DROP TABLE {};".format(self._name))
            print('Table deleted successfully.')

        self.c = self._conn.cursor()
        self.merged_list = []

    # create a table using the attrib names and types

    def create(self, attrb_names, attrb_types):

        # accepts two lists concatenates into one to use in sql create table command

        for i in range(len(attrb_names)):

            concat_list= attrb_names[i] + " " + attrb_types[i]

            self.merged_list.append(concat_list)

        # combines list into one string for sql statement
        sql_input = ', '.join(self.merged_list)

        # creates table in sqlite db file

        # .format converts variables from text file into string for sql command

        self.c.execute(''' CREATE TABLE {} ({})  '''.format(self._name, sql_input))

    # insert a row into the table

    def addRow(self, attrib_vals):

        self.c.execute('''INSERT INTO {} VALUES(?, ?, ?, ?, ?)'''.format(self._name), attrib_vals)

        self._conn.commit()


    # returns a cursor

    def retrieveAll(self):


        self.c.execute("SELECT * FROM {}".format(self._name))

        rows = self.c.fetchall()

        return rows

    # opens text file and inputs every line from text into a list

    # needs to be correct file path

with open('input file.txt') as f:
    print("Opened file successfully")

    mylist = f.read().splitlines()
    print(mylist)

get_table_name = mylist[0]

# initializes class object grabbing first item of list as table name
class_obj = table(get_table_name)

# separates list into two different lists

list_names = []

list_types = []

# this list is for place holders in insert command changes size depending on how many attributes from textfile
question_list = []

# these while loops create list of attribute names and data types
i = 1
while mylist[i] != "":

    list_names.append(mylist[i])
    i += 2


j = 2

while mylist[j] != "":

    list_types.append(mylist[j])
    j += 2

# this takes size of list of names to create enough place holders for insert sql command
k = 0
while k != len(list_names):
    question_list.append("?")

    k += 1

# this list and loop recognizes where records begin in text file seperate by blank lines then appends to a
# list of records

list_of_records = []
y = 0

while y != len(mylist):
    y += 1
    if mylist[y] == "":
        y += 1
        while y != len(mylist):
            y += 1
            if y >= len(mylist):
                break

            list_of_records.append(mylist[y])

# calls function to create table

class_obj.create(attrb_names=list_names, attrb_types=list_types)

print("New table created successfully")

# this part detects using place holder list how many lines are equal to one record using modulous
# then clears for next record to be inserted looping to add rows in db file

one_record = []
e = 0
while e != len(list_of_records):
    one_record.append(list_of_records[e])
    e += 1

    if e % len(question_list) == 0:

        class_obj.addRow(one_record)
        one_record.clear()

f.close()

# retrieves all records from db file

database = class_obj.retrieveAll()

# displays all records in db file to gui screen

master = Tk()

listbox = Listbox(master, bg="RED", bd="10", fg="BLUE", height="31", width="40")
listbox.pack(side=LEFT, fill=BOTH, expand=YES)

for item in database:
    listbox.insert(END, item)

mainloop()





