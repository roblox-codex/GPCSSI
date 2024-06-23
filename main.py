import streamlit as st
import pandas as pd
import numpy as np

def upload_cdr_file():
    uploaded_file = st.file_uploader("Upload your CDR file", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.write("Uploaded file column names:", df.columns.tolist())
        return df
    return None

def analyze_cdr(df):
    st.subheader("Analysis Results")
    
    if df is not None:
        st.write("Total records:", len(df))
        
        # Checking if necessary columns exist
        required_columns = ['DURATION', 'FIRST CELL ID A ADDRESS', 'IMEI A', 'ROAMING A', 'DATE', 'TIME']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns in the uploaded file: {', '.join(missing_columns)}")
            return

        try:
            max_call_idx = df['DURATION'].idxmax()
            max_location = df['FIRST CELL ID A ADDRESS'].value_counts().idxmax()
            max_imei = df['IMEI A'].value_counts().idxmax()
            max_duration = df['DURATION'].max()
            roaming_calls = df[df['ROAMING A'] == 'Yes']  # Assuming 'Yes' indicates roaming

            st.write("Max Call Duration Record:", df.loc[max_call_idx])
            st.write("Location with Max Calls:", max_location)
            st.write("Max Duration:", max_duration)
            st.write("IMEI with Max Calls:", max_imei)
            st.write("Number of Roaming Calls:", len(roaming_calls))

            df['DATE'] = pd.to_datetime(df['DATE'])
            daily_first_last_call = df.groupby(df['DATE'].dt.date).agg({'TIME': ['first', 'last']})
            daily_first_last_location = df.groupby(df['FIRST CELL ID A ADDRESS']).agg({'TIME': ['first', 'last']})
            
            st.write("Daily First and Last Call:", daily_first_last_call)
            st.write("Daily First and Last Location:", daily_first_last_location)
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
    else:
        st.write("No data to analyze.")

def main():
    st.title("CDR Analysis Tool")
    df = upload_cdr_file()
    if df is not None:
        st.write("CDR Data Preview:")
        st.dataframe(df.head())
        analyze_cdr(df)
    else:
        st.write("Please upload a CDR file to start analysis.")

if __name__ == "__main__":
    main()
