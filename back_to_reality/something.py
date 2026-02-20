import os
import matplotlib.pyplot as plt
import pandas as pd

from back_to_reality.connection import fetch_bitcoin_market_chart


def main() -> None:
    # Fetch approximately 5 years of daily BTC-USD data
    days = 365 * 5
    df = fetch_bitcoin_market_chart(vs_currency="usd", days=days)

    # Ensure the index is sorted just in case
    df = df.sort_index()

    # Compute 50-day and 200-day moving averages.
    # If there isn't enough history yet, the corresponding values will be NaN
    # and simply won't produce visible lines for that period.
    df["ma_50"] = df["price"].rolling(window=50, min_periods=50).mean()
    df["ma_200"] = df["price"].rolling(window=200, min_periods=200).mean()

    # Restrict to the last 5 years in case the API returned a bit more
    if len(df) > 0:
        last_timestamp = df.index.max()
        window_start = last_timestamp - pd.Timedelta(days=365 * 5)
        df = df[df.index >= window_start]

    current_row = df.iloc[-1]
    current_price = float(current_row["price"])
    current_ma_50 = float(current_row["ma_50"]) if pd.notna(current_row["ma_50"]) else None
    current_ma_200 = float(current_row["ma_200"]) if pd.notna(current_row["ma_200"]) else None

    # Print current values to the console
    print(f"Current BTC price (USD): {current_price:,.2f}")
    if current_ma_50 is not None:
        print(f"50-day moving average: {current_ma_50:,.2f} USD")
    else:
        print("50-day moving average: not enough data yet.")

    if current_ma_200 is not None:
        print(f"200-day moving average: {current_ma_200:,.2f} USD")
    else:
        print("200-day moving average: not enough data yet.")

    # Create a beautiful visualization
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(df.index, df["price"], label="BTC Price (USD)", color="#1f77b4", linewidth=1.5)

    if df["ma_50"].notna().any():
        ax.plot(
            df.index,
            df["ma_50"],
            label="50-day MA",
            color="#ff7f0e",
            linewidth=1.5,
        )

    if df["ma_200"].notna().any():
        ax.plot(
            df.index,
            df["ma_200"],
            label="200-day MA",
            color="#2ca02c",
            linewidth=1.5,
        )

    ax.set_title("Bitcoin (BTC-USD) Price with 50- and 200-Day Moving Averages\nLast 5 Years")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")

    # Format y-axis with thousands separator
    ax.ticklabel_format(style="plain", axis="y")

    # Add a text box showing the latest values
    info_lines = [f"Current price: ${current_price:,.2f}"]
    if current_ma_50 is not None:
        info_lines.append(f"50-day MA: ${current_ma_50:,.2f}")
    if current_ma_200 is not None:
        info_lines.append(f"200-day MA: ${current_ma_200:,.2f}")
    info_text = "\n".join(info_lines)

    ax.text(
        0.02,
        0.98,
        info_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    ax.legend()
    fig.autofmt_xdate()
    plt.tight_layout()

    # Ensure output directory exists and save figure there
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "btc_usd_5y_moving_averages.png")
    plt.savefig(output_path, dpi=300)


if __name__ == "__main__":
    main()

