import pandas as pd
import os

# Define the path where the CSV files are stored
path = './EBMF'  # Change to your path, e.g., '/Users/yourname/Desktop'

# Create a writer object from Pandas to write Excel files
writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')

# Loop through all files in the directory
for filename in os.listdir(path):
    if filename.endswith('.csv'):  # Check if the file is a CSV
        file_path = os.path.join(path, filename)
        df = pd.read_csv(file_path)  # Read the CSV file
        # Use the filename as the sheet name, stripping the '.csv' part
        df.to_excel(writer, sheet_name=os.path.splitext(filename)[0], index=False)

# Save the Excel file
writer.save()

print("Excel file created successfully!")
