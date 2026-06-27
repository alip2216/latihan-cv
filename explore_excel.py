import pandas as pd

excel_file = 'ecv_data.xlsx'
xls = pd.ExcelFile(excel_file)
print("Sheet names:", xls.sheet_names)

for sheet in xls.sheet_names:
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(xls, sheet_name=sheet)
    print("Columns:", list(df.columns))
    print(df.head(2).to_dict(orient='records'))
