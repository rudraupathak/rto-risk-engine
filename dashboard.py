import streamlit as st
import pandas as pd
import pickle

# Load the AI model directly into the dashboard
with open("rto_model.pkl", "rb") as file:
    model = pickle.load(file)

# Set up the page appearance
st.set_page_config(page_title="RTO Risk Engine", page_icon="🛡️", layout="centered")

st.title("🛡️ Dynamic Checkout Intent Engine")
st.markdown("This dashboard simulates a checkout page. The AI evaluates the user's risk in real-time before displaying the Cash-on-Delivery option.")
st.divider()

# Create a layout with two columns
col1, col2 = st.columns(2)

# Column 1: User Inputs
with col1:
    st.subheader("🛒 Checkout Details")
    cart_value = st.number_input("Cart Value (INR)", min_value=100, max_value=150000, value=2000, step=500)
    hour = st.slider("Checkout Hour (24h)", min_value=0, max_value=23, value=14)
    address_score = st.slider("Address Quality (1=Bad, 10=Perfect)", min_value=1, max_value=10, value=8)
    is_guest = st.selectbox("User Status", options=["Registered User", "Guest Checkout"])
    
    guest_int = 1 if is_guest == "Guest Checkout" else 0

# Column 2: The API Response & Dynamic UI
with col2:
    st.subheader("⚡ Live AI Decision")
    
    if st.button("Process Payment Options", use_container_width=True):
        
        # Format the data for the AI
        input_df = pd.DataFrame([{
            'Cart_Value_INR': cart_value,
            'Checkout_Hour': hour,
            'Address_Quality_Score': address_score,
            'Is_Guest_User': guest_int
        }])
        
        # Ask the AI for a prediction directly
        prediction = model.predict(input_df)[0]
        
        # Update the UI
        if prediction == 1:
            st.error("🚨 **High RTO Risk Detected**")
            st.write("High probability of Return to Origin. Force prepaid payment.")
            st.warning("💳 **Credit Card / UPI** (Required)")
        else:
            st.success("✅ **Low Risk User**")
            st.write("Safe transaction. Display all payment options.")
            st.info("💳 **Credit Card / UPI**")
            st.info("💵 **Cash on Delivery (COD)**")
