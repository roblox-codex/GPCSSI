import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def get_details(df):
    st.write("Choose an option:")
    option = st.selectbox("Select an option", ["Max Duration Details", "Details of last 7 days"])

    if option == "Max Duration Details":
        max_duration_details(df)
    elif option == "Details of last 7 days":
        last_7_days_details(df)

def max_duration_details(df):
    max_duration = df['DURATION'].max()
    max_duration_details = df[df['DURATION'] == max_duration]
    st.write("Max Duration Details:")
    st.write(max_duration_details)

def last_7_days_details(df):
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

    if df['DATE'].isna().any():
        st.warning("Some dates couldn't be parsed and are set to NaT.")
    
    st.write("Converted DATE column to datetime:")
    st.write(df['DATE'])
    
    last_7_days = datetime.now() - timedelta(days=7)
    st.write(f"Filtering records from: {last_7_days}")
    
    last_7_days_details = df[df['DATE'] >= last_7_days]
    st.write("Details of last 7 days:")
    st.write(last_7_days_details)

def main():
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        get_details(df)

if __name__ == "__main__":
    main()
