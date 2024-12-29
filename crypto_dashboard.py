import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def fetch_historical_data(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data[['Open', 'Close', 'High', 'Low']]

def process_monthly_prices(data):
    data['Average Price'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
    monthly_avg = data['Average Price'].resample('M').mean()
    return monthly_avg

def process_fluctuations(data):
    data['Fluctuation'] = data['High'] - data['Low']
    monthly_fluctuations = data['Fluctuation'].resample('M').mean()
    return monthly_fluctuations

# Define the Streamlit app
def main():
    st.title("Cryptocurrency Dashboard")
    st.sidebar.header("Settings")

    # Cryptocurrency list with symbols
    crypto_list = {
        'Arbitrum': 'ARB-USD',
        'Artificial Superintelligence Alliance': 'FET-USD',
        'Ethena': 'ENA-USD',
        'Algorand': 'ALGO-USD',
        'Filecoin': 'FIL-USD',
        'Kaspa': 'KAS-USD',
        'OKB': 'OKB-USD',
        'Fantom': 'FTM-USD',
        'Cosmos': 'ATOM-USD',
        'Virtuals Protocol': 'VIRTUAL-USD'
    }

    selected_crypto = st.sidebar.selectbox("Select Cryptocurrency", list(crypto_list.keys()))
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-25"))

    if st.sidebar.button("Fetch Data"):
        symbol = crypto_list[selected_crypto]
        try:
            st.write(f"Fetching data for {selected_crypto} ({symbol})...")
            data = fetch_historical_data(symbol, start_date, end_date)

            # Process data for average prices
            monthly_avg = process_monthly_prices(data)
            fluctuations = process_fluctuations(data)

            # Plot average price
            st.subheader(f"Monthly Average Prices - {selected_crypto}")
            st.line_chart(monthly_avg)

            # Plot fluctuations
            st.subheader(f"Monthly Price Fluctuations - {selected_crypto}")
            st.line_chart(fluctuations)

        except Exception as e:
            st.error(f"Failed to fetch data for {selected_crypto}: {e}")

if __name__ == "__main__":
    main()
