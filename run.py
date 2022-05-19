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
            print("Data is valid!")
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


def update_worksheet(data, worksheet):
    """
    Receive a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided.
    """  
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


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


def get_last_5_entries_sales():
    """
    Collects the columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    
    # Access a single col using col_values() from gspread:
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        # Use slice: to get last 5 entries.
        # Colin is used as we are slicing multiple els
        columns.append(column[-5:])
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    
    new_stock_data = []
    
    # Create a for loop to iterate through each column
    for column in data:
        # Convert values into integers 
        int_column = [int(num) for num in column]
        
        # Work out the averages:
        average = sum(int_column) / len(int_column)
        # Add 10% to average
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    # Creates a list comprehension to convert these values
    # into integers
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    return stock_data


print("Welcome to Love Sandwiches Data Automation")
stock_data = main()


# Write you code below this comment
def get_stock_values(data):
    """
    Print out the calculated stock numbers for each sandwich type.
    """
    headings = SHEET.worksheet("surplus").row_values(1)
    
    print("Make the following numbers of sandwiches for next market:\n")
    
    stock_dict = {}
    for head, stockdata in zip(headings, data):
        entry = {head: stockdata}
        stock_dict[head] = stockdata
    
    return stock_dict

    # return {heading: data for heading, data in zip(headings, data)}
   
 
stock_values = get_stock_values(stock_data)
print(stock_values)

