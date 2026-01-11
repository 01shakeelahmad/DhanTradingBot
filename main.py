import os
import pandas as pd
# CRITICAL: This line imports the necessary class from the library
from dhanhq import dhanhq 

# --- Configuration: Credentials updated with your token ---
CLIENT_ID = "YOUR_CLIENT_ID" # Keep your client ID here
# WARNING: Do not share this token publicly. 
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzY4MjE2MzYwLCJpYXQiOjE3NjgxMjk5NjAsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA5NDYwNDM1In0.OXJ86QgRKgFzCg4a45r1R9dbriYB1tOR6v0HJfcscsjvYk2YJstQNWYiis5xJqv_ZyxlHI0lwLljx2zIRGvKGA"
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
    print(f"Current Date: 2026-01-11")

    # --- 1. Define the stock and timeframe ---
    instrument_id = '2885' # Reliance Industries
    exchange_segment = 'NSE_EQ'
    
    try:
        # Function name corrected to 'historical_daily_data' with correct parameters
        historical_data = dhan.historical_daily_data(
            exchange_segment=exchange_segment,
            security_id=instrument_id, # Use security_id instead of instrument_id here
            instrument_type='EQUITY', # Add this new required parameter
            from_date='2025-05-01', 
            to_date='2026-01-11' # Current Date is January 11, 2026
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
    
    # Ensure there's enough data before accessing iloc[-1]
    if df_data.empty:
        print("Error: DataFrame is empty after processing.")
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
