import numpy as np
import pandas as pd
import pickle
import joblib
df=pd.read_csv('Dataset/names.csv')
rf_classifier=joblib.load('random_forest.joblib')
with open("label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
sc_loaded = joblib.load("scaler.pkl")
# df.drop(['Unnamed: 0','Damage','City','County','Community',"Street Name",'Street Number'],inplace=True,axis=1)
x=list(df['Columns'].unique())
# Define training columns (should match the features used for training)
train_cols = x  # Assuming 'x' is your original training DataFrame

# Define categorical columns that were label-encoded
cols_ = [
    "Hazard Type", "Structure Category", "Eaves", "Window Pane",
    "Deck/Porch On Grade", "Deck/Porch Elevated",
    "Patio Cover/Carport Attached to Structure", "Fence Attached to Structure"
]

# Example user input
user_input = {
    "Street Type (e.g. road, drive, lane, etc.)": "Avenue",  
    "State": "CA",  
    "CAL FIRE Unit": "LAC",  
    "Incident Name": "Quail",  
    "Hazard Type": "Fire",  
    "Structure Type": "Single Family Residence Multi Story",  
    "Structure Category": "Single Residence",  
    "Roof Construction": "Asphalt",  
    "Eaves": "Unenclosed",  
    "Vent Screen": "Unscreened",  
    "Exterior Siding": "Wood",  
    "Window Pane": "Single Pane",  
    "Deck/Porch On Grade": "Wood",  
    "Deck/Porch Elevated": "Wood",  
    "Patio Cover/Carport Attached to Structure": "Combustible",  
    "Fence Attached to Structure": "Combustible",  
    "Assessed Improved Value (parcel)": 500000,  
    "Year Built (parcel)": 1995,  
    "Latitude": 34.0522,  
    "Longitude": -118.2437  
}

# Initialize feature array
arr = np.zeros(len(train_cols))

# Encode input features
for key, value in user_input.items():
    if key in train_cols and key not in cols_:
        if isinstance(value,str):
            one_hot_key = f"{key}_{value}"
            if one_hot_key in train_cols:
             arr[train_cols.index(one_hot_key)] = 1
        else:
            arr[train_cols.index(key)] = value 
    elif key in cols_:  
        if value in label_encoders[key].classes_:  
            arr[train_cols.index(key)] = label_encoders[key].transform([value])[0]
        else:
            arr[train_cols.index(key)] = -1 

# Convert to DataFrame to match scaler's expected input format
arr_df = pd.DataFrame([arr], columns=train_cols)
arr_df.to_csv('demo.csv')
# Scale the numerical features
arr_scaled = sc_loaded.transform(arr_df)

# # Make prediction with RandomForestClassifier
prediction = rf_classifier.predict(arr_scaled)
print("Predicted Class:", prediction[0])
