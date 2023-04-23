import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)
conn = connect(credentials=credentials)
client=gspread.authorize(credentials)

sheet_id = '1RIfSn2L_HHdMpMoVWSuC_ejEVF4_8nB6oN3doT0RmY0'
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
database_df = pd.read_csv(csv_url, on_bad_lines='skip')

database_df = database_df.astype(str)
sheet_url = st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
sheet = client.open_by_url(sheet_url).sheet1
sheet.update([database_df.columns.values.tolist()] + database_df.values.tolist())
st.success('Data has been written to Google Sheets')