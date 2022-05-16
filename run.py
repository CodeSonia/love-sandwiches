# Imports the entire gspread library so we can access every
# class and function within it
import gspread

# Imports the Credentials class which is part of the
# service account function in the google auth libray
from google.oauth2.service_account import Credentials

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
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")

    # Using split() method to separate items from
    # the list
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all the string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    # Try statement will run if there are no errors
    # and data is valid
    try:
        [int(value) for value in values]
        # Check if th1e values are not 6 values
        if len(values) != 6:
            # Except statement will print an error to the
            # terminal
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}")        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_sales_data()
