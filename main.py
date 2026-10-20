
import pandas as pd
import matplotlib.pyplot as plt

# Load historical weather data
df = pd.read_csv("historical_weather.csv")

# Convert dates to datetime format
df["date"] = pd.to_datetime(df["date"])

# Plot temperatures
plt.figure(figsize=(10, 5))

plt.plot(
    df["date"],
    df["max_temp_c"],
    marker="o",
    label="Maximum Temperature"
)

plt.plot(
    df["date"],
    df["min_temp_c"],
    marker="o",
    label="Minimum Temperature"
)

plt.plot(
    df["date"],
    df["mean_temp_c"],
    marker="o",
    label="Average Temperature"
)

plt.title("Chennai Historical Temperature Analysis")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart as an image
plt.savefig("temperature_trend.png", dpi=300)
plt.show()

print("Temperature chart saved as temperature_trend.png")
