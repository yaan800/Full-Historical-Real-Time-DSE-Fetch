import pandas as pd
import streamlit as st
import requests

# -------------------------------
# Historical Excel Functions
# -------------------------------
def read_excel_safely(file):
    try:
        xls = pd.ExcelFile(file, engine='openpyxl')
    except Exception as e:
        st.error(f"Failed to read Excel file: {e}")
        return {}

    all_sheets = {}
    for sheet_name in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None, engine='openpyxl')
            all_sheets[sheet_name] = df
        except Exception as e:
            st.warning(f"Skipped sheet '{sheet_name}' due to error: {e}")
            continue
    return all_sheets


def process_sheet(df):
    if df.shape[1] < 7:
        st.warning("Sheet has fewer than 7 columns, skipping.")
        return None

    df = df.iloc[:, :7]
    df.columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    for col in ['Open','High','Low','Close','Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
    return df


# -------------------------------
# DSE Real-Time Fetch Function
# -------------------------------
def fetch_today_dse():
    """Fetch today's DSE prices"""
    url = "https://www.dsebd.org/latest_share_price_all.php"
    try:
        tables = pd.read_html(url)
        df = tables[0]
        df = df[['Symbol','LTP','High','Low','Close','YCP','Volume']]
        df.rename(columns={'Symbol':'Ticker','LTP':'Close'}, inplace=True)
        df['Date'] = pd.Timestamp.today()
        df['Open'] = df['Close']
        df = df[['Ticker','Date','Open','High','Low','Close','Volume']]
        return df
    except Exception as e:
        st.error(f"Failed to fetch DSE data: {e}")
        return pd.DataFrame()
