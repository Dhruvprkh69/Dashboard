import streamlit as st
import pandas as pd
from openchart import NSEData
import datetime
from datetime import timedelta

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Nifty 50 Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📊 Nifty 50 Dashboard")

# Initialize NSE data
nse = NSEData()

# Download NSE data first
with st.spinner("Downloading NSE data... This may take a few minutes."):
    nse.download()
st.success("NSE data download completed!")

# Function to fetch and process data for a single stock
def get_stock_data(symbol):
    try:
        end_date = datetime.datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Get today's data
        data = nse.historical(
            symbol=symbol,
            exchange='NSE',
            start=start_date,
            end=end_date,
            interval='1d'
        )
        
        if not data.empty and 'High' in data.columns and 'Low' in data.columns and 'Close' in data.columns:
            # Calculate metrics
            high_52w = data['High'].max()
            low_52w = data['Low'].min()
            current_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
            change_pct = ((current_price - prev_price) / prev_price) * 100
            
            return {
                'Symbol': symbol,
                'Price': round(current_price, 2),
                'Change': round(change_pct, 2),
                '52W High': round(high_52w, 2),
                '52W Low': round(low_52w, 2),
                'Down from High': round(((current_price - high_52w) / high_52w) * 100, 2)
            }
        else:
            st.warning(f"Data for {symbol} is incomplete or missing required columns")
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
    return None

# List of Nifty 50 companies
nifty50_symbols = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'ICICIBANK', 'INFY', 'HINDUNILVR', 'HDFC', 'SBIN',
    'BHARTIARTL', 'KOTAKBANK', 'BAJFINANCE', 'LICI', 'LT', 'HCLTECH', 'ASIANPAINT',
    'AXISBANK', 'MARUTI', 'SUNPHARMA', 'TITAN', 'ADANIENT', 'DMART', 'ULTRACEMCO',
    'BAJAJFINSV', 'WIPRO', 'ONGC', 'NTPC', 'JSWSTEEL', 'POWERGRID', 'M&M', 'TATASTEEL',
    'ADANIPORTS', 'COALINDIA', 'TECHM', 'TATAMOTORS', 'GRASIM', 'BRITANNIA', 'EICHERMOT',
    'ITC', 'HEROMOTOCO', 'DIVISLAB', 'DRREDDY', 'CIPLA', 'ADANIGREEN', 'HINDALCO',
    'SBILIFE', 'BAJAJ-AUTO', 'HDFCLIFE', 'UPL', 'BPCL', 'INDUSINDBK'
]

# Create a progress bar
progress_bar = st.progress(0)
status_text = st.empty()

# Fetch data for all companies
all_data = []
for i, symbol in enumerate(nifty50_symbols):
    status_text.text(f"Fetching data for {symbol}...")
    data = get_stock_data(symbol)
    if data:
        all_data.append(data)
    progress_bar.progress((i + 1) / len(nifty50_symbols))

# Clear the status text and progress bar
status_text.empty()
progress_bar.empty()

# Convert to DataFrame
if all_data:
    df = pd.DataFrame(all_data)
    
    # Function to format price with ₹ symbol
    def format_price(price):
        return f"₹{price:,.2f}"
    
    # Function to format change with arrow and color
    def format_change(change):
        arrow = "↑" if change > 0 else "↓"
        color = "green" if change > 0 else "red"
        return f'<span style="color: {color}">{arrow} {abs(change):.2f}%</span>'

    # Format the DataFrame
    formatted_df = df.copy()
    formatted_df['Price'] = formatted_df['Price'].apply(format_price)
    formatted_df['52W High'] = formatted_df['52W High'].apply(format_price)
    formatted_df['52W Low'] = formatted_df['52W Low'].apply(format_price)
    formatted_df['Change'] = formatted_df['Change'].apply(format_change)
    formatted_df['Down from High'] = formatted_df['Down from High'].apply(lambda x: f"{x:.2f}%")

    # Add custom CSS for table styling
    st.markdown("""
    <style>
    .dataframe {
        font-size: 14px !important;
        width: 100% !important;
        border-collapse: collapse !important;
    }
    .dataframe th {
        background-color: #1E1E1E !important;
        color: white !important;
        font-weight: bold !important;
        text-align: left !important;
        padding: 12px 8px !important;
        border: 1px solid #333 !important;
    }
    .dataframe td {
        padding: 10px 8px !important;
        border: 1px solid #ddd !important;
        background-color: #ffffff !important;
    }
    .dataframe tr:nth-child(even) td {
        background-color: #f8f9fa !important;
    }
    .dataframe tr:hover td {
        background-color: #f0f2f6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display the table
    st.write(formatted_df.to_html(
        columns=['Symbol', 'Price', 'Change', '52W High', '52W Low', 'Down from High'],
        escape=False,
        index=False
    ), unsafe_allow_html=True)

else:
    st.error("No data was successfully fetched for any stocks. Please check your internet connection and try again.")

# Add a footer
st.markdown("---")
st.markdown("Data source: NSE (National Stock Exchange of India)")
st.markdown("Last updated: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))