import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# 1. Load Data
df = pd.read_csv('car_data_updated.csv')

# 2. ENCODING (Exact Match for App)
fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2, 'LPG': 3, 'Electric': 4}
seller_map = {'Dealer': 0, 'Individual': 1, 'Trustmark Dealer': 0}
trans_map = {'Manual': 0, 'Automatic': 1}

df.replace({'Fuel_Type': fuel_map}, inplace=True)
df.replace({'Seller_Type': seller_map}, inplace=True)
df.replace({'Transmission': transmission_map}, inplace=True)

# 3. Train
X = df[['Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type', 'Transmission']]
y = df['Selling_Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

# 4. Save
with open('car_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Success! Model Reset.")
