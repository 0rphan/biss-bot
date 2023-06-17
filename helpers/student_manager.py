import db_manager
import csv
import asyncio

try:
    file = open("../database/.inited", 'r')
    exit()
except:
    pass

# In case the db does not exists create it here
asyncio.run(db_manager.init_db())

with open("../database/students.csv", 'r', encoding="utf8") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        break
    for row in csvreader:
        email = row[1]
        full_name = row[2]
        english_name = row[3]
        id = row[4]
        phone = row[5]
        birthday = row[-3]
        address = row[-2]
        asyncio.run(
            db_manager.add_student(id, "male", full_name, english_name, email,
                                   phone, address, birthday))

open("../database/.inited", 'w')
