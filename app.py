import streamlit as st
import requests
import pandas as pd
import os

# Set API Key (store securely in an .env file in production)
API_KEY = os.getenv("API_KEY")  # Ensure API key is stored securely

# Function to get sample stock data
def get_sample_stocks():
    return [
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "roe": 28.5},
        {"symbol": "MSFT", "name": "Microsoft Corp.", "sector": "Technology", "roe": 32.1},
        {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "roe": 18.3},
        {"symbol": "PG", "name": "Procter & Gamble", "sector": "Consumer Goods", "roe": 20.2},
    ]

# Function to fetch stock financial data from API
def fetch_stock_data(ticker):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]
    return {}

# Streamlit UI
st.title("📈 Stock Screener & Industry Leaders")

# Sidebar Navigation
st.sidebar.title("🔍 Choose a Tool")
option = st.sidebar.radio("Select a Feature:", ["Stock Screener", "Industry Leaders"])

if option == "Stock Screener":
    st.write("Filtering sample stocks with **ROE > 15%**.")
    stocks = get_sample_stocks()
    filtered_stocks = [stock for stock in stocks if stock['roe'] > 15]
    df = pd.DataFrame(filtered_stocks)
    st.write(f"✅ Total Filtered Stocks: {len(filtered_stocks)}")
    st.write("### 📊 Filtered Stocks")
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "filtered_stocks.csv", "text/csv")
    st.write("✅ Sample data used for testing.")

elif option == "Industry Leaders":
    st.write("### 🏆 Industry Leaders")
    uploaded_file = st.file_uploader("Upload Industry Leaders Excel File", type=["xlsx"])
    
    if uploaded_file:
        industry_df = pd.read_excel(uploaded_file)
        
        # Update data using API
        for index, row in industry_df.iterrows():
            ticker = row['Symbol']
            stock_data = fetch_stock_data(ticker)
            if stock_data:
                industry_df.at[index, 'Price'] = stock_data.get('price', 'N/A')
                industry_df.at[index, 'Market Cap'] = stock_data.get('mktCap', 'N/A')
                industry_df.at[index, 'P/E Ratio'] = stock_data.get('pe', 'N/A')

        st.dataframe(industry_df)
        csv = industry_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Updated CSV", csv, "industry_leaders.csv", "text/csv")
        st.write("✅ Data updated from Financial Modeling Prep API.")
    else:
        st.warning("⚠️ Please upload the Excel file to proceed.")

