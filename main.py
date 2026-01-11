import os
import pandas as pd
from dhanhq import dhanhq
from datetime import datetime, timedelta

# --- Configuration: Replace with your credentials ---
CLIENT_ID = "YOUR_CLIENT_ID" 
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN" 
# CRITICAL: Replace YOUR_CLIENT_ID and YOUR_ACCESS_TOKEN with your actual keys.
# Do not share your full token publicly. 
# -----------------------------------------------------------

dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

def calculate_ma(data, window=200):
    """Calculates a Simple Moving Average (SMA) using pandas."""
    df = pd.DataFrame(data['data'], columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['SMA_200'] = df['close'].rolling(window=window).mean()
    return df

def trade_strategy():
    """
    Automated trading logic: Checks if price crossed below 200-day MA.
    """
    print("Running automated trading strategy...")
    
    # Calculate dates dynamically
    today = datetime.now()
    # Fetch data up to yesterday's date to ensure data is complete
    to_date_str = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    # Fetch from ~300 days ago
    from_date_str = (today - timedelta(days=300)).strftime('%Y-%m-%d')

    print(f"Fetching data from {from_date_str} to {to_date_str}")


    # --- 1. Define the stock and timeframe ---
    instrument_id = '2885' # Example: Reliance Industries (Verify this ID on Dhan docs)
    exchange_segment = 'NSE_EQ'
    
    try:
        historical_data = dhan.historical_daily_data(
            exchange_segment=exchange_segment,
            security_id=instrument_id, 
            instrument_type='EQUITY',
            from_date=from_date_str,
            to_date=to_date_str
        )
        
        if 'data' not in historical_data or not historical_data['data']:
            print("Error: Historical data list is empty or invalid.")
            print(f"Raw Response: {historical_data}")
            return

    except Exception as e:
        print(f"Failed to fetch historical data: {e}")
        return

    # --- 2. Calculate the 200-day MA ---
    df_data = calculate_ma(historical_data, window=200)
    
    if df_data.empty:
        print("Error: DataFrame is empty after MA processing.")
        return

    last_close = df_data['close'].iloc[-1]
    last_ma = df_data['SMA_200'].iloc[-1]
    
    print(f"Current Close Price: {last_close}")
    print(f"200-day MA: {last_ma}")

    # --- 3. Check the trading condition (Price goes below MA) ---
    if last_close < last_ma:
        print("SIGNAL: Price crossed below 200-day MA. Initiating SELL order procedures.")
        # Place your SELL order code here 
    else:
        print("SIGNAL: No sell signal yet. Price is above the 200-day MA.")

    print("Strategy execution complete.")
    return {"message": "Strategy executed successfully"}

# This line is needed for the service to run the function
if __name__ == "__main__":
    trade_strategy()
