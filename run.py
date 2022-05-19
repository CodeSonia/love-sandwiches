# Imports the entire gspread library so we can access every
# class and function within it
import gspread

# Imports the Credentials class which is part of the
# service account function in the google auth libray
from google.oauth2.service_account import Credentials
from pprint import pprint

# All CAPS variable = constant variable
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Created settings to access data from the google sheet
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop with repeatedly request data, until it is valid.
    """  
    # Runs a while loop that asks the user for data
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        # Using split() method to separate items from
        # the list
        sales_data = data_str.split(",")
        validate_data(sales_data)
        # Use a if statement to call our validate data
        # function
        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        # Try statement will run if there are no errors
        # and data is valid
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    
    # Access our sales worksheet from our Google Sheet
    # Use gspead worksheet(). The value provided
    # is the name of the worksheet from our spreadsheet.
    sales_worksheet = SHEET.worksheet("sales")
    
    # Use another GSPREAD function: append()
    # This will add our data to the worksheet.
    sales_worksheet.append_row(data)
    print("Sales worksheet updates successfully.\n")


def update_surplus_worksheet(data):
    """
    Updates surplus worksheet, add enew row with the list data provided.
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully.\n")
  

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    
    # Get the stock worksheet. 
    # Use gspread get_all_values to fetch the data
    stock = SHEET.worksheet("stock").get_all_values()
    
    # Access the last row of the stock sheet.
    stock_row = stock[-1]
    
    # Create an empty list to add the surplus data
    surplus_data = []
    # Use a zip() to iterate 2 lists
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
        
    return surplus_data

# It is common practice to wrap the main function calls
# of a program within a function called main:


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    # Creates a list comprehension to convert these values
    # into integers
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)


print("Welcome to Love Sandwiches Data Automation")
main()