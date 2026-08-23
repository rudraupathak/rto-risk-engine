import streamlit as st
import requests

# Set up the page appearance
st.set_page_config(page_title="RTO Risk Engine", page_icon="🛡️", layout="centered")

st.title("🛡️ Dynamic Checkout Intent Engine")
st.markdown("This dashboard simulates a checkout page. The frontend communicates with a dedicated FastAPI microservice to evaluate risk in real time.")
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
        
        # 1. Format the data into a JSON payload for the network request
        payload = {
            "cart_value_inr": cart_value,
            "checkout_hour": hour,
            "address_quality_score": address_score,
            "is_guest_user": guest_int
        }
        
        # 2. This is your live Render API URL!
        API_URL = "https://rto-risk-engine.onrender.com/predict_risk"
        
        try:
            with st.spinner("Querying Risk Microservice..."):
                # 3. Send the data over the internet to Render
                response = requests.post(API_URL, json=payload, timeout=30)
                data = response.json()
            
            # 4. Update the UI based on what Render sends back
            if data["action"] == "hide_cod":
                st.error("🚨 **High RTO Risk Detected**")
                st.write(data["message"])
                st.warning("💳 **Credit Card / UPI** (Required)")
            else:
                st.success("✅ **Low Risk User**")
                st.write(data["message"])
                st.info("💳 **Credit Card / UPI**")
                st.info("💵 **Cash on Delivery (COD)**")
                
        except requests.exceptions.RequestException as e:
            st.error("Failed to connect to backend microservice.")
            st.caption(f"Details: {e}")
