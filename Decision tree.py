import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor


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
             "Relative Humidity Avg. (%)": "Humidity","Precip. Accumulated (mm)": "Precip", "Wind Speed 10 m Avg. (km/h)": "Wind_Speed",
             "Wind Dir. 10 m Avg. (°)": "Wind_Dir"})  # Rename column names

low_high_price = df_joined[(df_joined['Price'] == 0) | (df_joined['Price'] > 999)]

final = df_joined[(df_joined['Price'] > 50) & (df_joined['Price'] < 999)]

final_df = df_joined[['Date', 'Station Name', 'Price', 'Demand', 'Temp','Humidity','Precip','Wind_Speed','Wind_Dir']]

y = final['Price']
X = final[['Temp', 'Humidity','Precip','Wind_Speed', 'Wind_Dir']]

# Random Assignment of Training and Test (15%) Datasets (Regression Model)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=5)

# Fit Decision Tree Regression Model
DT = tree.DecisionTreeRegressor(random_state=123)
DT.fit(X_train, y_train)
DT_pred = DT.predict(X_test)
Rsq_DT = r2_score(y_test, DT_pred)

# Fit Random Forest Regression Model
RF = RandomForestRegressor(random_state=123)
RF.fit(X_train, y_train)
RF_pred = RF.predict(X_test)
Rsq_RF = r2_score(y_test, RF_pred)

# Create Actual vs. Predicted Plot
plt.figure()
plt.plot(y_test, y_test, '-')
plt.plot(DT_pred, y_test, '.', color="blue", label="DT", linewidth=2)
plt.plot(RF_pred, y_test, '.', color="red", label="RF", linewidth=2)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Tree-Based Regression Models")
plt.legend()
plt.show()

y1 = final['Price']
X1 = final[['Demand']]

# Random Assignment of Training and Test (15%) Datasets (Regression Model)
X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=0.15, random_state=5)

# Fit Decision Tree Regression Model
DT = tree.DecisionTreeRegressor(random_state=123)
DT.fit(X_train, y_train)
DT_pred = DT.predict(X_test)
Rsq_DT = r2_score(y_test, DT_pred)

# Fit Random Forest Regression Model
RF = RandomForestRegressor(random_state=123)
RF.fit(X_train, y_train)
RF_pred = RF.predict(X_test)
Rsq_RF = r2_score(y_test, RF_pred)

# Create Actual vs. Predicted Plot
plt.figure()
plt.plot(y_test, y_test, '-')
plt.plot(DT_pred, y_test, '.', color="blue", label="DT", linewidth=2)
plt.plot(RF_pred, y_test, '.', color="red", label="RF", linewidth=2)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Tree-Based Regression Models")
plt.legend()
plt.show()