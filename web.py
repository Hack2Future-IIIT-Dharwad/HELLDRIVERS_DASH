import streamlit as st
import csv
import json
import yaml
import requests
import pandas as pd
import pandas as pd
import automl
import secrets


def generate_random_key():
    return secrets.token_hex(8)
const1 = generate_random_key()
const2 = generate_random_key()
const3 = generate_random_key()
const4 = generate_random_key()
const5 = generate_random_key()

def main():
    
    
    st.title("Data Importer")

    st.subheader("Select Data Source")
    source = st.selectbox("Choose a data source", ["Upload CSV", "Upload JSON", "Upload YAML", "Enter API URL"])
    global data_placeholder 
    data_placeholder = st.empty()
    data = {}

    if source == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_file is not None:
            # Display a loading message while the data is being loaded
            data_placeholder.write("Loading data...")
            data = pd.read_csv(uploaded_file)
            # Update the placeholder with the loaded data
            data_placeholder.write(data)
    elif source == "Upload JSON":
        uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])
        if uploaded_file is not None:
            # Display a loading message while the data is being loaded
            data_placeholder.write("Loading data...")
            data = pd.read_json(uploaded_file)
            # Update the placeholder with the loaded data
            data_placeholder.write(data)
    elif source == "Upload YAML":
        uploaded_file = st.file_uploader("Choose a YAML file", type=["yaml"])
        if uploaded_file is not None:
            # Display a loading message while the data is being loaded
            data_placeholder.write("Loading data...")
            import yaml
            data = yaml.safe_load(uploaded_file)
            # Update the placeholder with the loaded data
            data_placeholder.write(data)
    elif source == "Enter API URL":
        api_url = st.text_input("Enter API URL")
        if api_url:
            # Display a loading message while the data is being loaded
            data_placeholder.write("Loading data...")
            import requests
            response = requests.get(api_url)
            data = response.json()
            # Update the placeholder with the loaded data
            data_placeholder.write(data)
    global csv_data
    if data is not None:
        csv_data = pd.DataFrame(data)
        side()
        prediction()
        csv_data.to_csv('hack.csv')
    return 0



def side():
    df = csv_data
    target_variable = df.columns
    target_variable2 = df.columns
    st.title("Choose the Target Variables")
    global X
    X = st.selectbox("Select the target variable",target_variable, key = const2 )
    print(X)
    global y
    y = None
    
    if st.button("Train", key = const4):
        print("calling training")
        automl.main2(X,y)
    return X, y

def prediction():
    prediction = None
    X_pred = None
    with st.form("prediction_form"):
        X_pred = st.text_input("Enter the input data to predict", key = const5)
        if st.form_submit_button("Make Prediction"):
            with st.spinner('Prediction in Progress. Please Wait...'):
                prediction = automl.predict(X_pred)
            st.success('Success! Click the Download button below to retrieve prediction results (JSON format')
            if prediction != None:
                st.write("The predicted value is", prediction)
    
