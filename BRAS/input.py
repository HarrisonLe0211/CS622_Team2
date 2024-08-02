import pandas as pd
df = pd.read_excel('GuestList.xlsx', engine="openpyxl",sheet_name="Sheet2")

print(df.loc[2,'Name']) #Read cell at row 2 of column "Name"
