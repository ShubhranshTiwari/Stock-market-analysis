from data_fetcher import get_stock_data
from visualizer import plot_price, plot_with_moving_averages
from statistics import calculate_basic_stats, print_stats
from inputs import get_user_inputs, get_feature_choices
from trend_analysis import detect_trend



def main():
    ticker, start, end = get_user_inputs()
    if not ticker:
        return

    data = get_stock_data(ticker, start, end)
    if data.empty:
        print("No data found. Please check your ticker and date range.")
        return

    choice = get_feature_choices()

    if choice == "1":
        stats = calculate_basic_stats(data)
        print_stats(stats)
    elif choice == "2":
        plot_price(data, ticker)
    elif choice == "3":
        plot_with_moving_averages(data, ticker)
    elif choice == "5":
        stats = calculate_basic_stats(data)
        print_stats(stats)
        plot_price(data, ticker)
        plot_with_moving_averages(data, ticker)
        trend = detect_trend(data)
        print("\n📉 Trend Analysis:")
        print(trend)
    elif choice == "4":
        trend = detect_trend(data)
        print("\n📉 Trend Analysis:")
        print(trend)
    elif choice == "6":
        print("Goodbye 👋")

    else:
        print("❌ Invalid choice. Exiting.")


if __name__ == "__main__":
    main()