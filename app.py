import streamlit as st
import pickle
import numpy as np
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Food Delivery Time Predictor",
    layout="wide"
)

# ---------------- BACKGROUND FUNCTION ----------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
    f"""
    <style>

    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
        url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        backdrop-filter: blur(6px);
        z-index:-1;
    }}

    /* MAIN TITLE */
    .main-title {{
        text-align:center;
        font-size:70px;
        font-weight:900;
        color:white;
        letter-spacing:1px;
    }}

    .subtitle {{
        text-align:center;
        font-size:20px;
        color:white;
        font-weight:600;
        margin-bottom:40px;
    }}

    /* SECTION TITLE */
    .section-title {{
        font-size:50px;
        font-weight:800;
        color:white;
        text-align:center;
        margin-bottom:20px;
    }}

    /* INPUT LABELS */
    label {{
        font-size:60px !important;
        font-weight:600 !important;
        color:white !important;
    }}

    /* PREDICTION CARD */
    .prediction-box {{
        background: rgba(128,128,128,0.75);
        color:white;
        padding:50px;
        border-radius:20px;
        text-align:center;
        font-size:30px;
        font-weight:bold;
        box-shadow:0px 10px 35px rgba(0,0,0,0.6);
    }}

    </style>
    """,
    unsafe_allow_html=True
    )

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("best_random_forest_model.pkl", "rb"))

# ---------------- SET BACKGROUND ----------------
set_bg("background.jpg")

# ---------------- TITLE ----------------
st.markdown('<p class="main-title"> Food Delivery Time Prediction</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Machine Learning Powered Delivery Time Estimator</p>', unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------- ORDER DETAILS ----------------
st.markdown('<p class="section-title"> Enter Order Details </p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    distance = st.slider("Distance (km)",0.5,20.0,5.0)

with col2:
    weather = st.selectbox(
        "Weather",
        ["Sunny","Rainy","Foggy","Stormy"]
    )

with col3:
    traffic = st.selectbox(
        "Traffic Level",
        ["Low","Medium","High"]
    )

with col4:
    vehicle = st.selectbox(
        "Vehicle Type",
        ["Bike","Scooter","Car"]
    )

with col5:
    prep_time = st.slider(
        "Preparation Time (min)",
        5,60,15
    )

st.write("")
st.write("")
st.write("")

# ---------------- ENCODING ----------------
weather_map = {
    "Sunny":0,
    "Rainy":1,
    "Foggy":2,
    "Stormy":3
}

traffic_map = {
    "Low":0,
    "Medium":1,
    "High":2
}

vehicle_map = {
    "Bike":0,
    "Scooter":1,
    "Car":2
}

weather_encoded = weather_map[weather]
traffic_encoded = traffic_map[traffic]
vehicle_encoded = vehicle_map[vehicle]

# ---------------- PREDICT BUTTON ----------------
center1, center2, center3 = st.columns([1,2,1])

with center2:
    predict = st.button(" Predict Delivery Time", use_container_width=True)

st.write("")
st.write("")
st.write("")

# ---------------- PREDICTION RESULT ----------------
if predict:

    features = np.array([[distance,
                          weather_encoded,
                          traffic_encoded,
                          vehicle_encoded,
                          prep_time]])

    prediction = model.predict(features)[0]

    st.markdown(f"""
    <div class="prediction-box">
    ⏱ Estimated Delivery Time<br><br>
    {round(prediction,2)} Minutes
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.write("")
st.write("---")

st.markdown(
"<p style='text-align:center;color:white;font-size:20px;font-weight:600;'>Developed by Aman Singh | Machine Learning Project</p>",
unsafe_allow_html=True
)