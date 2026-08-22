import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="RTO Risk Decision Engine")

# Load the model
with open("rto_model.pkl", "rb") as file:
    model = pickle.load(file)

class CheckoutData(BaseModel):
    cart_value_inr: int
    checkout_hour: int
    address_quality_score: int
    is_guest_user: int

@app.post("/predict_risk")
def predict_rto_risk(data: CheckoutData):
    input_df = pd.DataFrame([{
        'Cart_Value_INR': data.cart_value_inr,
        'Checkout_Hour': data.checkout_hour,
        'Address_Quality_Score': data.address_quality_score,
        'Is_Guest_User': data.is_guest_user
    }])
    
    prediction = model.predict(input_df)[0]
    
    if prediction == 1:
        return {"status": "high_risk", "action": "hide_cod"}
    else:
        return {"status": "low_risk", "action": "allow_cod"}