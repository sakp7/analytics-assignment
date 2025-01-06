# Required Libraries
import streamlit as st
import requests
import json

# Settingup configuration
BASE_API_URL='https://api.langflow.astra.datastax.com' 
LANGFLOW_ID ='2b0af0e3-10a9-4d98-8cff-e3db9d3ab7f0'
FLOW_ID =st.secrets['FLOW_ID']
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

# Pages
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

    # Title
    st.title("Social Media Analytics Module")
    
    # Project Overview
    st.header("Project Overview")
    st.write("""
    This **Social Media Analytics Module** analyzes engagement data from mock social media accounts. 
    It leverages **Groq's LLM model (Llama3.1-8b-instant)** for advanced natural language insights. 
    Built with **Streamlit** as the front end, the application is deployed on **Streamlit Cloud**, 
    providing an easy-to-use interface for analyzing and visualizing engagement metrics.
    """)
    
    # Tech Stack
    st.header("Tech Stack")
    
    st.subheader("Backend")
    st.write("""
    - **Groq LLM**: Llama3.1-8b-instant model for generating insights.
    - **Langflow**: Used to create workflows that integrate GPT models and automate data processing.
    - **DataStax Astra DB**: Cloud-based NoSQL database storing engagement metrics like likes, shares, comments, and post types.
    """)
    
    st.subheader("Frontend")
    st.write("""
    - **Streamlit**: Interactive front end for user input and real-time analytics display.
    """)
    
    st.subheader("Deployment")
    st.write("""
    - **Streamlit Cloud**: Seamless deployment platform making the app accessible over the internet.
    """)
    
    # Key Features
    st.header("Key Features")
    
    st.write("""
    1. **Social Media Insights**:
       - Accepts various post types (e.g., Carousels, Reels, Static Images).
       - Provides engagement metrics like likes, comments, shares, and saves.
       - Generates actionable insights such as: *"Reels have 2x higher comments than Static Images."*
    """)
    
    st.write("""
    2. **Data Fetching and Processing**:
       - Data is stored in **DataStax Astra DB**, simulating social media engagement metrics.
       - **Langflow** workflows fetch and analyze data using the Groq LLM model.
    """)
    
    st.write("""
    3. **Real-time Analytics**:
       - Insights are displayed dynamically on the Streamlit front end, offering up-to-date analytics as users select different post types.
    """)
    
    # Important Python Libraries
    st.header("Important Python Libraries")
    st.write("""
    - **Langflow**: For workflow creation and GPT model integration.
    - **Groq**: For leveraging the Llama3.1-8b-instant LLM model.
    - **DataStax**: For managing the cloud-based database.
    - **Streamlit**: For building the user interface and deploying the app.
    """)
    
    # Database
    st.header("Database")
    st.write("""
    The **sample database** in **DataStax Astra DB** stores simulated engagement data, including metrics for:
    - **Likes**
    - **Shares**
    - **Comments**
    - **Post Types (e.g., Reels, Carousels, Static Images)**
    
    The database is structured to efficiently fetch and calculate performance metrics for the analytics module.
    """)
    
    


# Navigation
home_page_instance = st.Page(home_page, title="Home")
description_page_instance = st.Page(description_page, title="Description")

# Navigation Logic
selected_page = st.navigation({"Home": [home_page_instance], "Description": [description_page_instance]})
selected_page.run()
