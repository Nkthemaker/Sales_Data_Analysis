import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
#Final
# Function Definitions
def fetch_historical_data(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data[['Open', 'Close', 'High', 'Low']]

def process_monthly_prices_by_year(data):
    data['Average Price'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
    data['Month'] = data.index.month
    data['Year'] = data.index.year
    return data.groupby(['Year', 'Month'])['Average Price'].mean().reset_index()


def process_monthly_prices(data):
    data['Average Price'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
    return data['Average Price'].resample('ME').mean()


def plot_monthly_comparisons(name, monthly_avg):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.figure(figsize=(12, 6))
    for year in monthly_avg['Year'].unique():
        yearly_data = monthly_avg[monthly_avg['Year'] == year]
        plt.plot(yearly_data['Month'], yearly_data['Average Price'], label=str(year))

    plt.xticks(range(1, 13), months)
    plt.title(f'Monthly Average Prices for {name} (Jan-Dec, Separated by Year)')
    plt.xlabel('Month')
    plt.ylabel('Average Price (USD)')
    plt.legend(title='Year')
    plt.grid(True)
    st.pyplot(plt)


def plot_monthly_prices(name, monthly_prices):
    plt.figure(figsize=(12, 6))
    monthly_prices.plot(label=name, marker='o')
    plt.title(f'Monthly Average Prices for {name}')
    plt.xlabel('Date')
    plt.ylabel('Average Price (USD)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)


# Streamlit UI
st.title("Cryptocurrency Dashboard")

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

start_date = st.date_input("Start Date", value=pd.to_datetime("2021-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2024-12-25"))

# Selection of Cryptocurrency
selected_crypto = st.selectbox("Select Cryptocurrency", list(crypto_list.keys()))

if selected_crypto:
    symbol = crypto_list[selected_crypto]
    st.subheader(f"Visualizations for {selected_crypto} ({symbol})")

    try:
        # Fetch and Process Data
        data = fetch_historical_data(symbol, start_date, end_date)
        data.index = pd.to_datetime(data.index)  # Ensure datetime index
        monthly_avg = process_monthly_prices_by_year(data)
        monthly_prices = process_monthly_prices(data)

        # Visualizations
        st.header(f"{selected_crypto} Monthly Price Chart")
        plot_monthly_prices(selected_crypto, monthly_prices)

        st.header(f"{selected_crypto} Year-Wise Monthly Comparison")
        plot_monthly_comparisons(selected_crypto, monthly_avg)

    except Exception as e:
        st.error(f"Failed to fetch or process data for {selected_crypto}: {e}")


