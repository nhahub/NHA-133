import streamlit as st
import pandas as pd
import pickle
import os
import xgboost as xgb
import numpy as np

# ========================= PAGE CONFIGURATION =========================
st.set_page_config(
    page_title="Car Price Prediction - Egypt",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========================= CUSTOM STYLING =========================
st.markdown("""
    <style>
    .main {
        padding: 2rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        font-size: 1.1rem;
        margin-top: 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 1rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .price-value {
        font-size: 3.5rem;
        font-weight: bold;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .price-label {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.95);
        margin-top: 0.5rem;
        font-weight: 500;
    }
    .input-group {
        margin-bottom: 1rem;
    }
    .input-label {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.3rem;
        font-size: 0.95rem;
        display: block;
    }
    .info-box {
        background-color: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        color: #065f46;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# ========================= CONFIGURATION =========================
MODEL_PATH = r"C:\Users\Nader\OneDrive\Desktop\xgbo_best_model.pkl"

EXPECTED_FEATURES = [
    "Make", "Model", "Year", "Mileage_in_KM", "Transmission", 
    "City", "Color", "Fuel_Type", "Body_Style"
]

# MinMaxScaler parameters from training
PRICE_MIN = 10000  # Minimum price from your data
PRICE_MAX = 5000000  # Maximum price from your data
CORRECTION_FACTOR = 0.85  # Adjust this to calibrate predictions (0.85 = reduce by 15%)

# Complete category lists from your dataset (99 Makes)
MAKE_LIST = [
    "Hyundai", "Ford", "BYD", "Kia", "Renault", "Jeep", "Seat", "Mercedes", "Chery", 
    "Jaguar", "Volkswagen", "Fiat", "Baic", "Chevrolet", "BMW", "Speranza", "Skoda", 
    "Nissan", "Mitsubishi", "Haval", "Opel", "Audi", "Peugeot", "Toyota", "Honda", 
    "MG", "Suzuki", "Daihatsu", "Dodge", "Citroen", "Daewoo", "Lada", "Porsche", 
    "Range Rover", "Land Rover", "Ssangyong", "Jac", "Brilliance", "Nasr", "Mini", 
    "Alfa Romeo", "Haima", "Jetour", "Changan", "Bentley", "Mazda", "Senova", "Proton", 
    "Forthing", "Ds", "Exeed", "Geely", "Mahindra", "Faw", "Volvo", "Subaru", "Gac", 
    "Gmc", "Cupra", "Bestune", "Zotye", "Cadillac", "Chana", "Infiniti", "Soueast", 
    "Ferrari", "Great Wall", "Changhe", "Saipa", "Dfsk", "Corvette", "Aston Martin", 
    "Chrysler", "Lamborghini", "Dongfeng Aeolus", "Isuzu", "Citroën", "Avatr", 
    "Maserati", "Abarth", "Hafei", "Tesla", "Keyton", "Zeekr", "Ssang Yong", 
    "Dongfeng", "Foton", "Kenbo", "Xpeng", "Victory", "Rox", "Sokon", "Kgm", 
    "Kyc", "Emgrand", "Slingshot", "Smart", "Lifan", "Other"
]

# Top 100 most common models for better UX
MODEL_LIST = [
    "Elantra HD", "Focus", "Song Plus", "Kuga", "Sportage", "Logan", "Wrangler", 
    "Carnival", "Ibiza", "Elantra Cn7", "Glb 200", "Tiggo 7", "F-Pace", "Passat", 
    "C180", "Tipo", "Tucson Nx4E", "U5 Plus", "Camaro", "Glc 200", "E 180", "120I", 
    "Liberty", "Tiguan", "Elantra AD", "A516", "Megane", "Karoq", "Kadjar", "Sentra", 
    "Eclipse", "Captur", "Unknown", "Gla 180", "Ecosport", "Lancer", "S320", "Bravo", 
    "Accent", "Vectra", "Sandero", "Xceed", "Glc 300 Coupe", "Tucson", "Yaris", 
    "Cr-V", "Qashqai", "Arrizo 5", "E350", "ZS", "Grand Vitara", "Cerato", "Verna", 
    "Golf", "Astra", "Octavia", "Renegade", "Corolla", "320i", "Cross Land", "Terios", 
    "Ram", "Ix 35", "C3 Aircross", "Kodiaq", "Swift", "Lacetti", "Grand Cherokee", 
    "Jetta", "Glc 300", "Ciaz", "Sunny", "Fortuner", "C-Elysee", "Granta", "Avante", 
    "Carens", "A35", "Rapid", "Lancer Puma", "Macan", "Civic", "Lanos", "Lanos Ii", 
    "A113", "C200", "Optra", "520I", "Tarraco", "Fusion", "E200", "V 250", "320I", 
    "C300", "Evoque", "E300", "Velar", "528I", "Duster", "New Range Rover", "Other"
]

TRANSMISSIONS = ["automatic", "manual"]

# Top 80 most common cities
CITY_LIST = [
    "Cairo", "Giza", "Alexandria", "Mansoura", "Qalyubia", "Dakahlia", "Ismailia", 
    "Gharbia", "Monufia", "Kafr El Sheikh", "Beheira", "Port Said", "Damietta", 
    "Suez", "Qena", "Asyut", "Sohag", "Eastern", "Hurghada", "Red Sea", "Matrouh", 
    "Helwan", "Fayoum", "Sharm El Sheikh", "Minya", "Bani Sweif", "Aswan", "Luxor", 
    "South Sinai", "Safaga", "October", "Sheikh Zayed City", "Haram", "Hadayek October", 
    "Badr City", "Ain Shams", "Obour City", "Dokki", "Manial", "Tanta", "Shorouk", 
    "Sharqia", "Warraq", "Marg", "Mahalla", "Pyramids Gardens", "Shibin El Kom", 
    "Zefta", "Shibin El Qanater", "Sadat City", "Bilbeis", "10Th Of Ramadan", "Shobra", 
    "Salam City", "Katameya", "Agamy", "Zamalek", "Borg El Arab", "Mohandessin", 
    "Sheraton", "Zagazig", "Damanhur", "Banha", "Qalyub", "Rosetta", "Tala", 
    "Kafr El Zayat", "Ashmoun", "Menouf", "Shibin Al Kawm", "Nasr City", "Other"
]

COLOR_LIST = [
    "Black", "White", "Gray", "Silver", "Brown", "Maroon", "Navy Blue", "Red", 
    "Blue", "Cream", "Gold", "Dark Grey", "Bronze", "Green", "Turquoise", "Champagne", 
    "Baby Blue", "Purple", "Orange", "Yellow", "Petroleum", "Mocha", "Olive", 
    "Cyan", "Dark Green", "Eggplant", "Other"
]

FUEL_LIST = ["Petrol", "Diesel", "Hybrid", "Electric", "CNG", "Natural Gas"]

BODY_LIST = [
    "Sedan", "Hatchback", "SUV", "Crossover", "Coupe", "Wagon", 
    "Pickup", "Van", "Convertible", "Minivan", "Microbus"
]

# ========================= HELPER FUNCTIONS =========================
@st.cache_resource
def load_predictor(path):
    """Load model with comprehensive error handling"""
    if not os.path.exists(path):
        st.error(f"❌ Model file not found at: `{path}`")
        st.info("Please ensure the model file exists at the specified path.")
        return None
    
    try:
        with open(path, "rb") as f:
            loaded = pickle.load(f)
        
        # Extract predictor from tuple/list if necessary
        if isinstance(loaded, (tuple, list)):
            for el in reversed(loaded):
                if hasattr(el, "predict"):
                    return el
            return loaded[-1] if loaded else None
        
        if hasattr(loaded, "predict"):
            return loaded
        
        st.error("❌ Loaded object does not have a predict() method.")
        return None
        
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

def inverse_transform_price(scaled_price):
    """Convert scaled price (0-1) back to actual EGP using MinMaxScaler formula"""
    # Formula: actual_price = scaled_price * (max - min) + min
    raw_price = scaled_price * (PRICE_MAX - PRICE_MIN) + PRICE_MIN
    # Apply correction factor to calibrate predictions
    return raw_price * CORRECTION_FACTOR

def build_input_df(make, model_name, year, mileage, transmission, city, color, fuel, body):
    """Build properly formatted input DataFrame"""
    row = {
        "Make": make,
        "Model": model_name,
        "Year": int(year),
        "Mileage_in_KM": float(mileage),
        "Transmission": transmission,
        "City": city,
        "Color": color,
        "Fuel_Type": fuel,
        "Body_Style": body,
    }
    
    df = pd.DataFrame([row], columns=EXPECTED_FEATURES)
    
    # Apply categorical encoding with training categories
    df["Make"] = pd.Categorical(df["Make"], categories=MAKE_LIST)
    df["Model"] = pd.Categorical(df["Model"], categories=MODEL_LIST)
    df["Transmission"] = pd.Categorical(df["Transmission"], categories=TRANSMISSIONS)
    df["City"] = pd.Categorical(df["City"], categories=CITY_LIST)
    df["Color"] = pd.Categorical(df["Color"], categories=COLOR_LIST)
    df["Fuel_Type"] = pd.Categorical(df["Fuel_Type"], categories=FUEL_LIST)
    df["Body_Style"] = pd.Categorical(df["Body_Style"], categories=BODY_LIST)
    
    # Numeric columns
    df["Year"] = df["Year"].astype(int)
    df["Mileage_in_KM"] = df["Mileage_in_KM"].astype(float)
    
    return df

def predict_price(predictor, X, show_debug=False):
    """Make prediction with fallback mechanism and optional debugging"""
    if show_debug:
        st.write("**Debug: Input DataFrame**")
        st.dataframe(pd.DataFrame({"Value": X.iloc[0].values}, index=X.columns))
        st.write("**Debug: Column Data Types**")
        st.write(X.dtypes.astype(str).to_dict())
    
    # Primary prediction attempt
    try:
        preds = predictor.predict(X)
        return float(preds[0]) if hasattr(preds, "__len__") else float(preds)
    except Exception as e1:
        if show_debug:
            st.warning(f"⚠️ Primary predict() failed: {str(e1)}")
            st.info("Attempting fallback using Booster + DMatrix...")
        
        # Fallback: use underlying Booster with DMatrix
        try:
            booster = None
            if hasattr(predictor, "get_booster"):
                booster = predictor.get_booster()
            elif isinstance(predictor, xgb.core.Booster):
                booster = predictor
            elif hasattr(predictor, "booster_"):
                booster = predictor.booster_
            
            if booster is None:
                raise ValueError("No Booster found in predictor")
            
            dmat = xgb.DMatrix(X, enable_categorical=True)
            preds = booster.predict(dmat)
            return float(preds[0]) if hasattr(preds, "__len__") else float(preds)
            
        except Exception as e2:
            st.error(f"❌ Prediction failed: {str(e2)}")
            st.info("""
            **Possible solutions:**
            1. Ensure the model expects categorical columns (not one-hot encoded)
            2. Verify category lists match training data exactly
            3. Check if model was saved with a preprocessing pipeline
            4. Try re-training with `enable_categorical=True` in XGBoost
            """)
            st.stop()

# ========================= MAIN APPLICATION =========================
st.title("🚗 Car Price Prediction")
st.markdown("### Professional price estimation for used cars in Egypt")

# Load model
predictor = load_predictor(MODEL_PATH)
if predictor is None:
    st.stop()

# Success indicator
st.markdown('<div class="success-box">✅ Model loaded successfully</div>', unsafe_allow_html=True)

# Optional: Show model info in sidebar
with st.sidebar:
    st.header("ℹ️ Model Information")
    st.write(f"**Model Path:** `{os.path.basename(MODEL_PATH)}`")
    
    try:
        if hasattr(predictor, "get_booster"):
            booster = predictor.get_booster()
            if booster and hasattr(booster, "feature_names"):
                st.write(f"**Features:** {len(booster.feature_names)}")
        elif hasattr(predictor, "feature_names_in_"):
            st.write(f"**Features:** {len(predictor.feature_names_in_)}")
    except:
        pass
    
    st.markdown("---")
    show_debug = st.checkbox("🔍 Show debug information", value=False)

st.markdown("---")

# ========================= INPUT FORM =========================
with st.form("prediction_form"):
    st.subheader("📝 Enter Car Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="input-label">🏭 Make (Brand)</p>', unsafe_allow_html=True)
        make = st.selectbox("Make", MAKE_LIST, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">📅 Year</p>', unsafe_allow_html=True)
        year = st.number_input("Year", min_value=1990, max_value=2026, value=2020, 
                               step=1, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">⚙️ Transmission</p>', unsafe_allow_html=True)
        transmission = st.selectbox("Transmission", TRANSMISSIONS, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">🎨 Color</p>', unsafe_allow_html=True)
        color = st.selectbox("Color", COLOR_LIST, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">🚙 Body Style</p>', unsafe_allow_html=True)
        body_style = st.selectbox("Body Style", BODY_LIST, label_visibility="collapsed")
    
    with col2:
        st.markdown('<p class="input-label">🚘 Model</p>', unsafe_allow_html=True)
        model_name = st.selectbox("Model", MODEL_LIST, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">📏 Mileage (KM)</p>', unsafe_allow_html=True)
        mileage = st.number_input("Mileage", min_value=0, max_value=1000000, 
                                  value=50000, step=1000, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">📍 City</p>', unsafe_allow_html=True)
        city = st.selectbox("City", CITY_LIST, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">⛽ Fuel Type</p>', unsafe_allow_html=True)
        fuel = st.selectbox("Fuel Type", FUEL_LIST, label_visibility="collapsed")
    
    # Submit button
    submitted = st.form_submit_button("🔮 Predict Price")

# ========================= PREDICTION =========================
if submitted:
    with st.spinner("🔄 Calculating price..."):
        # Build input DataFrame
        X = build_input_df(make, model_name, year, mileage, transmission, 
                          city, color, fuel, body_style)
        
        # Make prediction
        raw_pred = predict_price(predictor, X, show_debug=show_debug)
        
        # Convert scaled prediction (0-1) back to actual EGP
        final_price_egp = inverse_transform_price(raw_pred)
        
        # Display result
        st.markdown(f"""
            <div class="price-card">
                <p class="price-value">{int(final_price_egp):,}</p>
                <p class="price-label">Estimated Price (EGP)</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Additional details in expander
        with st.expander("📊 View Detailed Information"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Input Summary**")
                st.write(f"• Make: **{make}**")
                st.write(f"• Model: **{model_name}**")
                st.write(f"• Year: **{year}**")
                st.write(f"• Mileage: **{mileage:,} KM**")
                st.write(f"• Transmission: **{transmission}**")
            
            with col2:
                st.markdown("**🎯 Car Specifications**")
                st.write(f"• City: **{city}**")
                st.write(f"• Color: **{color}**")
                st.write(f"• Fuel: **{fuel}**")
                st.write(f"• Body: **{body_style}**")
            
            st.markdown("---")
            st.markdown("**💰 Price Breakdown**")
            st.write(f"• Scaled Prediction: **{raw_pred:.6f}** (0-1 range)")
            st.write(f"• Final Price: **{int(final_price_egp)}** EGP")
            st.write(f"• Formatted: **{int(final_price_egp):,}** EGP")

# ========================= FOOTER =========================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
        <p>💡 <strong>Tip:</strong> Ensure all inputs are accurate for best prediction results</p>
        <p>📊 Based on Egyptian used car market data | Powered by XGBoost</p>
    </div>
""", unsafe_allow_html=True)