import os
from dhanhq import dhanhq

# --- Configuration: Replace with your actual credentials ---
CLIENT_ID = "YOUR_CLIENT_ID" 
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
# -----------------------------------------------------------

dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

def trade_strategy():
    """
    Your automated trading logic goes here.
    This function will be run by the Render service.
    """
    print("Running automated trading strategy...")

    market_status = dhan.market_status()
    print(f"Market status: {market_status.get('msg', 'Unknown')}")
    
    # --- This is where we will add the 200-day MA logic later ---

    print("Strategy execution complete.")
    return {"message": "Strategy executed successfully"}

# This line is needed for the service to run the function
if __name__ == "__main__":
    trade_strategy()
