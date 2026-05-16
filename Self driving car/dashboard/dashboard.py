import streamlit as st

st.title("🚗 Self Driving Car Dashboard")

speed = st.slider("Speed", 0, 100, 50)
steering = st.slider("Steering", -1.0, 1.0, 0.0)

st.write(f"Speed: {speed}")
st.write(f"Steering: {steering}")
