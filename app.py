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

# Streamlit UI
st.title("📈 Simple Stock Screener")
st.write("Filtering sample stocks with **ROE > 15%**.")

# Fetch Sample Stocks
stocks = get_sample_stocks()
filtered_stocks = [stock for stock in stocks if stock['roe'] > 15]

st.write(f"✅ Total Filtered Stocks: {len(filtered_stocks)}")  # Debug print

# Convert to DataFrame
df = pd.DataFrame(filtered_stocks)

# Display table in Streamlit
st.write("### 📊 Filtered Stocks")
st.dataframe(df)

# Allow CSV Download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "filtered_stocks.csv", "text/csv")

st.write("✅ Sample data used for testing.")


