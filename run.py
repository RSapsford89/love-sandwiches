import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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

    return sales_data

def validate_data(values):
    """
    Validate the data as being int values in each position
    """
    try:
        for item in values:
            convert_to_int=int(item)
        
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values must be entered, you provied {len(values)}"
            )
        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False
    else:
        print("Values are valid.\n")
        return True




def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus data.

    Surplus is defined as: stock - sales = surplus
    and can positive or negative. Postive is waste, negative
    extra made once stock sold out
    """
    print("Calculating surplus...")
    stock = SHEET.worksheet("stock").get_all_values()
    #pprint(stock)
    stock_row = stock[-1]
    print(f"Sales row: {sales_row}")
    print(f"Stock row: {stock_row}")

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    print(f"Surplus data: {surplus_data}")
    return surplus_data

# Following 2 functions have been refactored into 
# update_worksheet and are here for reference
# def update_sales_worksheet(data):
#     """
#     Update the sales worksheet (google doc sheet). 
#     Add new row, insert list data provided
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet= SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated succesfully\n")


# def update_surplus_worksheet(surplus_list):
#     """
#     update the surplus sheet with 
#     """
#     print("Gathering surplus data...\n")
#     surplus= SHEET.worksheet("surplus").get_all_values()
#     print(surplus[-1])
#     surplus.append(surplus_list)
#     print("Surplus sheet updated with today's values.\n")

def update_worksheet(data,worksheet):
    """
    Receives a list of integers to be inserted into a worksheet.
    Update the releveant sheets with provided data.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update= SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated succesfully\n")

def get_last_5_entries_sales():
    """
    Get the last 5 entries from Sales sheet for all sandwhiches
    as a list of lists [] []
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Create an average of the 5 entries and round to a whole
    number and increase value by 10% to drive sales harder
    """
    print(("calculating stock data...\n"))
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        #sum(int_column)/5 also works when you know the length will never vary
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run all program functions
    """
    data=get_sales_data()
    sales_data=[int(num) for num in data]
    update_worksheet(sales_data,"sales")
    surplus_data=calculate_surplus_data(sales_data)
    update_worksheet(surplus_data,"surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data,"stock")
print("Welcome to Love Sandwiches automation!")
main()

#split the string on ',' X
#check length is 6 items
#check items are number
#stock - sales = surplus can be +ve or -ve