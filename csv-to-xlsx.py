import pandas as pd

# Load the CSV file
csv_file_path = '/mnt/data/greenhouse_candidates_after_2022-01-01.csv'
df = pd.read_csv(csv_file_path)

# Save the DataFrame to an Excel file
excel_file_path = '/mnt/data/greenhouse_candidates_after_2022-01-01.xlsx'
df.to_excel(excel_file_path, index=False)

# Confirm the file path for the user
excel_file_path
