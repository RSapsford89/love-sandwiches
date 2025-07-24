import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
        sales_data = data_str.split(',')
        #print(f"The data provided is {sales_data}")
        
        if validate_data(sales_data):
            print("Data is valid")
            break


def validate_data(sales_data):
    """
    Validate the data as being int values in each position
    """
    try:
        for item in sales_data:
            convert_to_int=int(item)
        
        if len(sales_data) != 6:
            raise ValueError(
                f"Exactly 6 values must be entered, you provied {len(sales_data)}"
            )
        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False
    else:
        print("Values are valid.\n")
        return True



data=get_sales_data()

#split the string on ',' X
#check length is 6 items
#check items are number