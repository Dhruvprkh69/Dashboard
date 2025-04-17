# Nifty 50 Dashboard

A Streamlit-based dashboard that displays key metrics for the top 50 companies in the Nifty 50 index.

## Features

- Real-time data for Nifty 50 companies
- 52-week high and low prices
- Top and bottom performers analysis
- Interactive price charts
- Distance from 52-week high/low calculations

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run nifty50_dashboard.py
```

2. The dashboard will open in your default web browser

## Dashboard Components

- **Top Performers**: Shows companies closest to their 52-week high
- **Bottom Performers**: Shows companies farthest from their 52-week low
- **Stock Price Analysis**: Interactive chart showing 52-week price movement for selected stocks

## Data Source

The data is fetched from the National Stock Exchange (NSE) using the openchart library.

## Note

The dashboard may take a few moments to load as it fetches real-time data for all 50 companies. 