import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_excel("HistoricalPoolPrice.xlsx")
df2 = pd.read_excel("ACISCALGARY.xlsx")

df2 = df2.rename(columns={"Date (Local Standard Time)": "Date"})  # Rename column names


# Standardize date column format
df1['Date'] = pd.to_datetime(df1['Date']).dt.strftime('%Y-%m-%d')  # Standardize date column format
df2['Date'] = pd.to_datetime(df2['Date']).dt.strftime('%Y-%m-%d')  # Standardize date column format

df_joined = pd.merge(df1, df2, how='left', on='Date')

summary = df_joined.describe(include='all')

df_joined = df_joined.drop(columns=['Date_Begin_GMT','Date_Begin_Local','ACTUAL_POOL_PRICE','ACTUAL_AIL','Air Temp. Min. (°C)','Air Temp. Max. (°C)'])

df_joined = df_joined.rename(columns={"Daily Average Price": "Price", "Daily Average Demand": "Demand", "Air Temp. Avg. (°C)": "Temp",
             "Relative Humidity Avg. (%)": "Humidity", "Wind Speed 10 m Avg. (km/h)": "Wind_Speed",
             "Wind Dir. 10 m Avg. (°)": "Wind_Dir"})  # Rename column names
low_high_price = df_joined[(df_joined['Price'] == 0) | (df_joined['Price'] > 999)]
final = df_joined[(df_joined['Price'] > 50) & (df_joined['Price'] < 500)]
final_df = df_joined[['Date', 'Station Name', 'Price', 'Demand', 'Temp','Humidity','Wind_Speed','Wind_Dir']]

# Create a figure with a 2x3 grid layout and adjust size as needed
fig_width, fig_height = 10, 6
plt.figure(figsize=(fig_width, fig_height))

# Define subplot positions in a 2x3 grid
plt.subplot(2, 3, 1)
plt.hist(final_df['Price'], bins=10, label='Price')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.grid(True)
plt.title('Price Distribution')

plt.subplot(2, 3, 2)
plt.hist(final_df['Demand'], bins=10, label='Demand')
plt.xlabel('Demand')
plt.ylabel('Frequency')
plt.grid(True)
plt.title('Demand Distribution')

plt.subplot(2, 3, 3)
plt.hist(final_df['Temp'], bins=10, label='Temperature')
plt.xlabel('Temperature')
plt.ylabel('Frequency')
plt.grid(True)
plt.title('Temperature Distribution')

plt.subplot(2, 3, 4)
plt.hist(final_df['Humidity'], bins=10, label='Humidity')
plt.xlabel('Humidity')
plt.ylabel('Frequency')
plt.grid(True)
plt.title('Humidity Distribution')

plt.subplot(2, 3, 5)
plt.hist(final_df['Wind_Speed'], bins=10, label='Wind Speed')
plt.xlabel('Wind Speed')
plt.ylabel('Frequency')
plt.grid(True)
plt.title('Wind Speed Distribution')

plt.subplot(2, 3, 6)
plt.hist(final_df['Wind_Dir'], bins=10, label='Wind Direction')
plt.xlabel('Wind Direction')
plt.ylabel('Frequency')
plt.grid(True)
plt.title('Wind Direction Distribution')

# Add legends
plt.subplots_adjust(bottom=0.1)
plt.legend()

plt.tight_layout()
plt.show()

