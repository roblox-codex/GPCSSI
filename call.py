import pandas as pd
from datetime import datetime, timedelta

def load_excel():
    file_path = input("Enter the path to the Excel file: ")
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def get_details(df):
    print("Choose an option:")
    print("1. Max Duration Details")
    print("2. Details of last 7 days")
    choice = input("Enter the option number: ")

    if choice == '1':
        max_duration_details(df)
    elif choice == '2':
        last_7_days_details(df)
    else:
        print("Invalid choice")

def max_duration_details(df):
    max_duration = df['DURATION'].max()
    max_duration_details = df[df['DURATION'] == max_duration]
    print("Max Duration Details:")
    print(max_duration_details)

def last_7_days_details(df):

    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
 
    if df['DATE'].isna().any():
        print("Warning: Some dates couldn't be parsed and are set to NaT.")
    
    print("Converted DATE column to datetime:")
    print(df['DATE'])
    
    last_7_days = datetime.now() - timedelta(days=7)
    print(f"Filtering records from: {last_7_days}")
    
    last_7_days_details = df[df['DATE'] >= last_7_days]
    print("Details of last 7 days:")
    print(last_7_days_details)

def main():
    df = load_excel()
    if df is not None:
        get_details(df)

if __name__ == "__main__":
    main()
