import streamlit as st
import pickle
import pandas as pd
import time

# --- CONFIGURATION ---
st.set_page_config(layout="centered", page_title="AutoValue", page_icon="🚘")

# --- GLASS UI CSS ---
st.markdown("""
    <style>
    /* Background Image */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=2583&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Dark Overlay */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
    }
    /* Text Colors */
    h1, h2, p, label { color: white !important; }
    
    /* Input Fields */
    .stNumberInput, .stSelectbox, .stSlider {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
        color: white !important;
    }
    
    /* RESULT BOX (Clean & Center) */
    .result-box {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #00d2ff;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.3);
        animation: fadeIn 1s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .big-price {
        font-size: 60px;
        font-weight: bold;
        color: #00d2ff;
        text-shadow: 0 0 15px #00d2ff;
        margin-top: 10px;
    }
    .small-label {
        font-size: 18px;
        color: #ddd;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* BUTTON */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        color: white;
        border-radius: 50px;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        width: 100%;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD FILES ---
try:
    model = pickle.load(open('car_model.pkl', 'rb'))
    car_data = pd.read_csv('car_data_updated.csv')
    car_names = car_data['Car_Name'].unique()
except:
    st.error("⚠️ Files missing. Run train_model.py first.")
    st.stop()

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>🚘 AutoValue Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>AI-Powered Valuation Engine</p>", unsafe_allow_html=True)

# --- INPUT FORM ---
col1, col2 = st.columns(2)

with col1:
    selected_car_name = st.selectbox("Select Car Model", car_names)
    
    # Auto-fill Logic
    avg_price = car_data[car_data['Car_Name'] == selected_car_name]['Present_Price'].mean()
    
    present_price = st.number_input("Showroom Price (Lakhs)", value=float(avg_price))
    year = st.slider("Manufacturing Year", 2000, 2025, 2018)

with col2:
    fuel_type = st.selectbox("Fuel Type", ('Petrol', 'Diesel', 'CNG', 'LPG', 'Electric'))
    kms_driven = st.number_input("Kilometers Driven", value=20000, step=1000)
    seller_type = st.selectbox("Seller", ('Dealer', 'Individual', 'Trustmark Dealer'))
    transmission = st.selectbox("Transmission", ('Manual', 'Automatic'))

st.write("") # Spacer

# --- CALCULATION LOGIC ---
if st.button("CALCULATE PRICE"):
    
    with st.spinner("Analyzing market data..."):
        time.sleep(0.8) # Animation delay

    # 1. Prepare Data
    fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2, 'LPG': 3, 'Electric': 4}
    seller_map = {'Dealer': 0, 'Individual': 1, 'Trustmark Dealer': 0}
    trans_map = {'Manual': 0, 'Automatic': 1}

    input_data = pd.DataFrame([[
        year, present_price, kms_driven, 
        fuel_map.get(fuel_type, 0), 
        seller_map.get(seller_type, 0), 
        trans_map.get(transmission, 0)
    ]], columns=['Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type', 'Transmission'])
    
    # 2. Predict
    prediction = model.predict(input_data)
    result_lakhs = prediction[0]
    
    # 3. Display Result (Clean Version)
    if result_lakhs < 0:
        st.error("⚠️ The inputs provided resulted in a negative value. Please check Year/Price.")
    else:
        st.markdown(f"""
            <div class="result-box">
                <div class="small-label">ESTIMATED MARKET VALUE</div>
                <div class="big-price">₹ {result_lakhs:.2f} Lakhs</div>
            </div>
        """, unsafe_allow_html=True)
        st.balloons()
