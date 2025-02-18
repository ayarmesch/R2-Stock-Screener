import streamlit as st
import requests
import pandas as pd
import os

# Set API Key (store securely in an .env file in production)
API_KEY = os.getenv("API_KEY")  # Ensure API key is stored securely

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

if option == "Industry Leaders":
    st.write("### 🏆 Industry Leaders")
    
    # Initialize or load industry leaders dataset
    if 'industry_leaders' not in st.session_state:
        st.session_state.industry_leaders = pd.DataFrame(columns=["Symbol", "Company Name", "Yield", "PE Ratio", "Price", "Sector", "Allocation", "Investment Amount", "Shares"])
    
    # Input form to add a new stock
    with st.form("add_stock"):
        col1, col2, col3 = st.columns(3)
        with col1:
            symbol = st.text_input("Stock Symbol:")
            company_name = st.text_input("Company Name:")
            sector = st.text_input("Sector:")
        with col2:
            allocation = st.number_input("Allocation (%)", min_value=1, max_value=100, value=8)
            investment_amount = st.number_input("Investment Amount ($)", min_value=1000, value=6400)
        with col3:
            shares = st.number_input("Shares", min_value=1, value=10)
        submitted = st.form_submit_button("Add/Update Stock")
        
        if submitted and symbol:
            stock_data = fetch_stock_data(symbol)
            new_row = {
                "Symbol": symbol,
                "Company Name": company_name,
                "Yield": stock_data.get('yield', 'N/A'),
                "PE Ratio": stock_data.get('pe', 'N/A'),
                "Price": stock_data.get('price', 'N/A'),
                "Sector": sector,
                "Allocation": f"{allocation}%",
                "Investment Amount": f"${investment_amount}",
                "Shares": shares
            }
            st.session_state.industry_leaders = pd.concat([st.session_state.industry_leaders, pd.DataFrame([new_row])], ignore_index=True)
    
    # Option to remove stocks
    if not st.session_state.industry_leaders.empty:
        remove_symbol = st.selectbox("Remove a stock:", [""] + list(st.session_state.industry_leaders["Symbol"]))
        if st.button("Remove Stock") and remove_symbol:
            st.session_state.industry_leaders = st.session_state.industry_leaders[st.session_state.industry_leaders["Symbol"] != remove_symbol]
    
    # Display and update data
    st.dataframe(st.session_state.industry_leaders)
    csv = st.session_state.industry_leaders.to_csv(index=False).encode('utf-8')
    st.download_button("Download Updated CSV", csv, "industry_leaders.csv", "text/csv")
    st.write("✅ Data updated from Financial Modeling Prep API.")


