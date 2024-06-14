import pandas as pd

# Static file address for now. Will need to change so that it will accept input from file selection interface. Will need logic to process whether file is
# a .xlsx file or .xls.
path = ("./static/excel/masterInventory8-2020.xlsx")

# Open the workbook and set up the sheet.
try:
    xlsx = pd.ExcelFile(path)
    sheet = xlsx.parse(0)
except:
    print("[ERROR]: File not found.")

# Iterate through first row in Excel sheet.
nrow,ncol = sheet.shape # nrow contains the number of rows, ncol contains the number of columns.

# Searches program for "drawing #" which indicates the start of the data.
def find_headers():
    try:
        for row in range(nrow):
            for col in range(ncol): 
                if "drawing #" in str(sheet.iloc[row,col]).lower():
                    draw_addr = [row,col]
                    for i in range(ncol):
                        if "description" in str(sheet.iloc[row,i]).lower():
                            desc_addr = [row,i]
                    # Process can be repeated for other Headers.
                    return draw_addr, desc_addr
        return(None,None)
    except:
        print("[ERROR]: Headers not found.")

def iterate_columns(draw_addr,desc_addr):
    for col in range(draw_addr[0]+1,nrow):
        if not pd.isnull(sheet.iloc[col,draw_addr[1]]) and not pd.isnull(sheet.iloc[col,desc_addr[1]]):
            print(sheet.iloc[col,desc_addr[1]])

# Main Method.
def main():
    draw_addr, desc_addr = find_headers() # drow and dcol will be used to store the addresses of the first item in the excel sheet.
    iterate_columns(draw_addr, desc_addr)

main()