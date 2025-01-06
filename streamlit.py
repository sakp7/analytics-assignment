# Required Libraries
import streamlit as st
import requests
import json

# Settingup configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "2b0af0e3-10a9-4d98-8cff-e3db9d3ab7f0"
FLOW_ID = "81ea3e8f-a341-4984-a749-098e3c60ebe0"
APPLICATION_TOKEN =st.secrets['auth_token']
ENDPOINT = ""

st.set_page_config(
    page_title="Analytics Bot - Team Sakp7",
    layout="centered",
    initial_sidebar_state="expanded",
    
)

TWEAKS = {
    "ChatInput-n63ev": {},
    "ChatOutput-IJlVz": {},
    "File-ciN11": {},
    "SplitText-ATIis": {},
    "AstraDB-mHggC": {},
    "Google Generative AI Embeddings-jhHuX": {},
    "GoogleGenerativeAIModel-qj4sw": {},
    "ParseData-hhAUA": {},
    "Prompt-tSdvR": {}
}

def run_flow(message: str, endpoint: str = ENDPOINT or FLOW_ID, tweaks: dict = TWEAKS) -> dict:
    """
    Runs the LangFlow with the given message and tweaks.

    :param message: Input message to send to the flow
    :param endpoint: Flow endpoint ID or name
    :param tweaks: Dictionary for custom tweaks
    :return: JSON response from the LangFlow API
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": "chat",  
        "input_type": "chat",
        "tweaks": tweaks
    }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

# Define Pages
def home_page():
    st.title("Social Media Engagement Analysis Bot")
    st.subheader("Analyze engagement on different types of posts")

    col1, col2, col3 = st.columns(3)
    a1 = col1.button("Engagement on Reels", key="b1")
    a2 = col2.button("Engagement on Carousels", key="b2")
    a3 = col3.button("Engagement on Static Images", key="b3")
    col4, col5, col6 = st.columns(3)
    a4 = col4.button("Reels VS Carousels")
    a5 = col5.button("Carousels VS Static Images")
    a6 = col6.button("Static Images VS Reels")

    # Custom message input
    message = st.text_input("Enter your custom query", placeholder="Type your query here...")

    if st.button("Generate Analysis"):
        if not message.strip():
            st.error("Please enter a valid message.")
        else:
            with st.spinner("Running the flow..."):
                result = run_flow(message)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.text("Output:")
                st.text(result["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"])

    # Button handlers
    def handle_query(query):
        with st.spinner("Running the flow..."):
            result = run_flow(query)
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.text("Output:")
            st.text(result["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"])

    if a1:
        handle_query("Reel")
    if a2:
        handle_query("Carousel")
    if a3:
        handle_query("Static Image")
    if a4:
        handle_query("Reels VS Carousel")
    if a5:
        handle_query("Carousels VS Static Images")
    if a6:
        handle_query("Static Images VS Reels")


def description_page():
    st.title("Description")
    st.markdown(
        """
        ### About this Application
        This application is designed to analyze social media engagement metrics. 
        You can compare the performance of various post types like:
        - **Reels**
        - **Carousels**
        - **Static Images**

        #### Features:
        - Predefined queries to analyze engagement.
        - Custom input support for generating insights.
        - Powered by LangFlow for natural language processing.

        #### Use Cases:
        - Social media analytics.
        - Campaign performance tracking.
        - Data-driven content strategy optimization.
        """
    )

# Navigation
home_page_instance = st.Page(home_page, title="Home")
description_page_instance = st.Page(description_page, title="Description")

# Navigation Logic
selected_page = st.navigation({"Home": [home_page_instance], "Description": [description_page_instance]})
selected_page.run()
