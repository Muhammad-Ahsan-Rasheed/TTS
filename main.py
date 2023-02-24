import streamlit as st
import streamlit_analytics
import requests

# Define the URL of the Flask app
flask_app_url = 'http://localhost:5000'

# Wrap the Flask app in a Streamlit app using the streamlit_analytics.streamlit_wrapper() function
st_app = streamlit_analytics.streamlit_wrapper(flask_app_url)

# Run the Streamlit app
if __name__ == '__main__':
    st_app.run()