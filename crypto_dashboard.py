import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set Streamlit layout to be centered
st.set_page_config(layout="wide", page_title="Cryptocurrency Dashboard")

# Custom CSS for centering the dashboard
# Add custom CSS to center the content
st.markdown(
    """
    <style>
    .main-content {
        max-width: 1000px;  /* Adjust the width as needed */
        margin: auto;      /* Center the content */
    }
    </style>
    <div class="main-content">
    """,
    unsafe_allow_html=True
)



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
    return data['Average Price'].resample('M').mean()


def find_best_week(data, month):
    data['Week'] = data.index.isocalendar().week
    data['Month'] = data.index.month
    data['Year'] = data.index.year
    monthly_data = data[data['Month'] == month]
    weekly_avg = monthly_data.groupby(['Year', 'Week']).apply(
        lambda x: (x['Open'] + x['Close'] + x['High'] + x['Low']).mean()
    ).reset_index(name='Average Price')
    best_week = weekly_avg.loc[weekly_avg['Average Price'].idxmax()]
    return best_week


def plot_monthly_comparisons(name, monthly_avg):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.figure(figsize=(10, 5))
    for year in monthly_avg['Year'].unique():
        yearly_data = monthly_avg[monthly_avg['Year'] == year]
        plt.plot(yearly_data['Month'], yearly_data['Average Price'], label=str(year), marker='o')

    plt.xticks(range(1, 13), months)
    plt.title(f'Monthly Average Prices for {name} (Jan-Dec, All Years)')
    plt.xlabel('Month')
    plt.ylabel('Average Price (USD)')
    plt.legend(title='Year')
    plt.grid(True)
    st.pyplot(plt)



def plot_selected_month_comparison(data, selected_month):
    plt.figure(figsize=(10, 5))
    for year in data['Year'].unique():
        yearly_month_data = data[(data['Month'] == selected_month) & (data['Year'] == year)]
        plt.plot(yearly_month_data.index.day, yearly_month_data['Average Price'], label=f'{year}', marker='o')

    plt.title(f'Day-by-Day Price Comparison for Month {selected_month}')
    plt.xlabel('Day of the Month')
    plt.ylabel('Average Price (USD)')
    plt.legend(title='Year')
    plt.grid(True)
    st.pyplot(plt)


def plot_best_week_comparison(data, title):
    plt.figure(figsize=(10, 5))
    for _, row in data.iterrows():
        label = f"Week {row['Week']} ({row['Year']})"
        plt.bar(label, row['Average Price'], label=label)
    plt.title(title)
    plt.xlabel('Week (Year)')
    plt.ylabel('Average Price (USD)')
    plt.grid(axis='y')
    plt.legend()
    st.pyplot(plt)


def plot_monthly_prices(name, monthly_prices):
    plt.figure(figsize=(10, 5))
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

selected_crypto = st.selectbox("Select Cryptocurrency", list(crypto_list.keys()))

if selected_crypto:
    symbol = crypto_list[selected_crypto]
    st.subheader(f"Visualizations for {selected_crypto} ({symbol})")

    try:
        # Fetch and Process Data
        data = fetch_historical_data(symbol, start_date, end_date)
        data.index = pd.to_datetime(data.index)
        data['Average Price'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
        data['Month'] = data.index.month
        data['Year'] = data.index.year
        monthly_prices = process_monthly_prices(data)
        monthly_avg = process_monthly_prices_by_year(data)

        col1, col2 = st.columns(2)

        with col1:
            # Visualizations
            st.subheader(f"{selected_crypto} Monthly Price Chart")
            plot_monthly_prices(selected_crypto, monthly_prices)
        with col2:
            # Monthly Comparison Chart
            st.subheader(f"{selected_crypto} Year-Wise Monthly Comparison")
            plot_monthly_comparisons(selected_crypto, monthly_avg)

        # Best Performing Week
        st.subheader("Advanced Analysis")
        selected_month = st.selectbox("Select Month", list(range(1, 13)), format_func=lambda x:
        ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][x - 1])
        best_week = find_best_week(data, selected_month)
        st.write(
            f"Best Week for {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][selected_month - 1]}: "
            f"Week {int(best_week['Week'])}, {int(best_week['Year'])}, Average Price: {best_week['Average Price']:.2f}")

        col3, col4 = st.columns(2)
        # Selected Month Day-by-Day Comparison
        with col3:
            st.subheader(
                f"Day-by-Day Price Comparison for {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][selected_month - 1]}")
            plot_selected_month_comparison(data, selected_month)

        with col4:

            # Best Weeks Comparison Across Years
            st.subheader("Comparison of Best Performing Weeks Across Years")
            weekly_data = data.groupby(['Year', 'Week']).apply(
                lambda x: (x['Open'] + x['Close'] + x['High'] + x['Low']).mean()
            ).reset_index(name='Average Price')
            best_weeks = weekly_data.groupby('Year').apply(lambda x: x.loc[x['Average Price'].idxmax()]).reset_index(
                drop=True)
            plot_best_week_comparison(best_weeks, f"Best Weeks for All Years ({selected_crypto})")

    except Exception as e:
        st.error(f"Failed to process data for {selected_crypto}: {e}")
