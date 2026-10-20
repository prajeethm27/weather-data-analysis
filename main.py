
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
from pathlib import Path

# Project settings
CITY = "Chennai"
LATITUDE = 13.0827
LONGITUDE = 80.2707

OUTPUT_DIR = Path(__file__).parent

def fetch_current_weather():
    """Fetch current weather and save it to CSV."""
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,wind_speed_10m"
        ),
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    current = data["current"]

    df = pd.DataFrame([{
        "city": CITY,
        "time": current["time"],
        "temperature_c": current["temperature_2m"],
        "feels_like_c": current["apparent_temperature"],
        "humidity_percent": current["relative_humidity_2m"],
        "wind_speed_kmh": current["wind_speed_10m"]
    }])

    df.to_csv(OUTPUT_DIR / "weather_data.csv", index=False)

    print("\nCURRENT WEATHER")
    print(df.to_string(index=False))
    print("Saved: weather_data.csv")


def fetch_historical_weather():
    """Fetch seven complete days of historical weather."""
    end_date = date.today() - timedelta(days=5)
    start_date = end_date - timedelta(days=6)

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "temperature_2m_mean,precipitation_sum"
        ),
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    daily = response.json()["daily"]

    df = pd.DataFrame({
        "date": daily["time"],
        "max_temp_c": daily["temperature_2m_max"],
        "min_temp_c": daily["temperature_2m_min"],
        "mean_temp_c": daily["temperature_2m_mean"],
        "precipitation_mm": daily["precipitation_sum"]
    })

    df.to_csv(OUTPUT_DIR / "historical_weather.csv", index=False)

    print("\nHISTORICAL WEATHER")
    print(df.to_string(index=False))
    print("Saved: historical_weather.csv")

    return df


def create_temperature_chart(df):
    """Plot and save historical temperature trends."""
    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["date"], df["max_temp_c"],
        marker="o", label="Maximum"
    )
    plt.plot(
        df["date"], df["min_temp_c"],
        marker="o", label="Minimum"
    )
    plt.plot(
        df["date"], df["mean_temp_c"],
        marker="o", label="Mean"
    )

    plt.title(f"{CITY} Historical Temperature Analysis")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_path = OUTPUT_DIR / "temperature_trend.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()

    print(f"\nChart saved: {chart_path.name}")


def main():
    print("=" * 40)
    print("WEATHER DATA ANALYSIS")
    print("=" * 40)

    try:
        fetch_current_weather()
        historical_df = fetch_historical_weather()
        create_temperature_chart(historical_df)

        print("\nSuccess! All project outputs are updated.")

    except requests.RequestException as error:
        print("\nNetwork or weather API error:")
        print(error)

    except (KeyError, TypeError, ValueError) as error:
        print("\nCould not process the weather data:")
        print(error)


if __name__ == "__main__":
    main()
