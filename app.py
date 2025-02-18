import streamlit as st
import requests
import pandas as pd
import os

# Set API Key (store securely in an .env file in production)
API_KEY = os.getenv("YPdL1uAS7P5Pr7TLb64e5cho0L4tFZrS")  # Ensure API key is stored securely

# Function to get S&P 500 company data
def get_sp500_companies():
    url = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        st.write("✅ Fetched S&P 500 companies:", data[:5])  # Print first 5 companies
        return data
    else:
        st.error(f"❌ Error fetching S&P 500 data: {response.text}")
        return []


# Function to get ROE data for a company
def get_roe_history(ticker):
    url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        st.write(f"✅ {ticker} ROE Data:", data[:5])  # Print first 5 ROE entries
        return {entry['date']: round(entry['returnOnEquity'], 2) for entry in data[:10]}
    else:
        st.error(f"❌ Error fetching ROE for {ticker}: {response.text}")
        return {}


# Streamlit UI
st.title("📈 High ROE Stock Screener")
st.write("Filtering S&P 500 stocks with **ROE > 15%** over the last 10 years.")

# Fetch S&P 500 companies
sp500_companies = get_sp500_companies()
filtered_stocks = []

# Screen for stocks with ROE > 15% for all 10 years
for company in sp500_companies:
    ticker = company['symbol']
    roe_history = get_roe_history(ticker)
    if roe_history and all(roe > 15 for roe in roe_history.values()):
        filtered_stocks.append({"Ticker": ticker, "Company": company['name'], **roe_history})

# Convert to DataFrame
df = pd.DataFrame(filtered_stocks)

# Display table in Streamlit
st.write("### 📊 Filtered High-ROE Stocks")
st.dataframe(df)

# Allow CSV Download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "high_roe_stocks.csv", "text/csv")

st.write("✅ Data sourced from Financial Modeling Prep API.")
