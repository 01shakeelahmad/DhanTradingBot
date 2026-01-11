# ... (imports and credentials remain the same) ...

dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

# ... (calculate_ma function remains the same) ...

def trade_strategy():
    # ... (print statements remain the same) ...

    # --- 1. Define the stock and timeframe ---
    instrument_id = '2885' # Reliance Industries
    exchange_segment = 'NSE_EQ'
    
    try:
        historical_data = dhan.historical_daily_data(
            exchange_segment=exchange_segment,
            security_id=instrument_id,
            instrument_type='EQUITY',
            from_date='2025-05-01', 
            to_date='2026-01-11'
        )
        
        # Add this line to debug:
        print(f"Raw Historical Data Response: {historical_data}") 

        if 'data' not in historical_data or not historical_data['data']: # Check if 'data' list is empty
            print("Error: Historical data list is empty. Cannot calculate MA.")
            return

    except Exception as e:
        print(f"Failed to fetch historical data: {e}")
        return

    # --- 2. Calculate the 200-day MA ---
    df_data = calculate_ma(historical_data, window=200)
    
    # These lines are causing the error because the DataFrame is likely empty:
    # last_close = df_data['close'].iloc[-1]
    # last_ma = df_data['SMA_200'].iloc[-1]
    
    print(f"DataFrame shape after calculation: {df_data.shape}")

    # ... (rest of the code remains commented out for now) ...

# ... (if __name__ == "__main__": trade_strategy() remains the same) ...
