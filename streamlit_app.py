import streamlit as st
import requests
from requests.exceptions import ConnectionError

ip_api = "170.168.101.56"
port_api = "5026"

st.title("Titanic Survival Prediction")

st.write("Enter the passenger details:")

# List to chose ticket class
pclass = st.selectbox("Ticket Class (Pclass)", [1,2,3])

#Text field to enter age with number validation
age = st.text_input("Age", value=10)
if not age.isdigit():
    st.error("Please enter a valid number of Age.")

#Text field to enter fare with number validation (ticket price)
fare = st.text_input("Fare", value=100)
if not fare.isdigit():
    st.error("Please enter a valid number of Fare.")

#Button to predict the survival
if st.button("Predict Survival"):
    if age.isdigit() and fare.isdigit():   
        try:
            url = f"http://{ip_api}:{port_api}/predict_model"
            payload = {"Pclass": pclass, "Age": int(age), "Fare": int(fare)}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Survival Prediction: {result['prediction']}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except ConnectionError:
            st.error("Failed to connect to the API")
    else:
        st.error("Please enter valid numbers for Age and Fare.")
    
#source .venv/bin/activate
#pip install streamlit requests
#streamlit run streamlit_app.py