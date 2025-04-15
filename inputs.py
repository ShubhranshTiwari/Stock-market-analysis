from datetime import datetime

def get_user_inputs():
    print("\n📈 Welcome to the Stock Market Analysis Tool!")

    ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
    if not ticker:
        ticker = "AAPL"

    start = input("Start date (YYYY-MM-DD) [default: 2023-01-01]: ").strip()
    if not start:
        start = "2023-01-01"

    end = input("End date (YYYY-MM-DD) [default: today]: ").strip()
    if not end:
        end = datetime.today().strftime('%Y-%m-%d')

    try:
        datetime.strptime(start, '%Y-%m-%d')
        datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return None, None, None

    return ticker, start, end

def get_feature_choices():
    print("\nWhat would you like to do?")
    print("1. Show basic statistics")
    print("2. Plot closing price")
    print("3. Plot moving averages")
    print("4. Analyze trend direction")
    print("5. Do all of the above")
    print("6. Exit")

    choice = input("Choose an option (1-6): ").strip()
    return choice
