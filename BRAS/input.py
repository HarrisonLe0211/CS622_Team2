import openpyxl

# Load the workbook and select the active worksheet
workbook = openpyxl.load_workbook('GuestList.xlsx')
sheet = workbook.active

# Reading from a specific cell
cell_value = sheet['A1'].value  # Reads the value of cell A1
print(f"Value in A1: {cell_value}")

# Writing to a specific cell
#sheet['B2'] = 'Hello, World!'  # Writes 'Hello, World!' into cell B2

import openpyxl

def read_and_write_excel(file_path):
    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # User input for reading a cell
    read_cell = input("Enter the cell address to read (e.g., A1): ")
    cell_value = sheet[read_cell].value
    print(f"Value in {read_cell}: {cell_value}")

    # User input for writing to a cell
    write_cell = input("Enter the cell address to write to (e.g., B2): ")
    write_value = input("Enter the value to write: ")
    sheet[write_cell] = write_value

    # Save the workbook with the changes
    workbook.save(file_path)
    print(f"Value '{write_value}' has been written to {write_cell} in {file_path}")

# Example usage
file_path = 'GuestList.xlsx'  # Replace with your file path

run = True

while run:
    
    read_and_write_excel(file_path)
    print("Continue?")
    command = input()
    if command == 'N':
        run = False
        print("exiting")

