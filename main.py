import streamlit as st
import pandas as pd
from utils import read_excel_safely, process_sheet, fetch_today_dse

st.set_page_config(page_title="DSE Real-Time Analyzer", layout="wide")
st.title("📈 DSE Stock Analysis – Real-Time Version")

# -------------------
# Step 1: Upload Historical Data
# -------------------
historical_file = st.file_uploader("Upload Historical Excel File", type="xlsx")
all_data = pd.DataFrame()

if historical_file:
    all_sheets = read_excel_safely(historical_file)
    if all_sheets:
        all_data = pd.concat([process_sheet(df) for df in all_sheets.values() if process_sheet(df) is not None], ignore_index=True)
        st.success(f"Loaded historical data: {len(all_data)} rows.")

# -------------------
# Step 2: Fetch Today’s DSE Data
# -------------------
if st.button("Fetch Today's DSE Data"):
    today_df = fetch_today_dse()
    if not today_df.empty:
        all_data = pd.concat([all_data, today_df], ignore_index=True)
        st.success("Today's DSE data fetched and merged!")

if not all_data.empty:
    st.subheader("Combined Dataset Preview")
    st.dataframe(all_data.head(50))
