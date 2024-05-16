import sqlite3
from openpyxl import Workbook


conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM library")
data = cursor.fetchall()


conn.close()

# Create a new Excel workbook
wb = Workbook()
ws = wb.active

# Write the headers
ws.append(['borrower', 'book', 'days'])

# write the data rows
for row in data:
    ws.append(row)

# Save the file
wb.save('library.xlsx')