import streamlit as st
import requests
import json

# Configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "2b0af0e3-10a9-4d98-8cff-e3db9d3ab7f0"
FLOW_ID = "81ea3e8f-a341-4984-a749-098e3c60ebe0"

APPLICATION_TOKEN ='AstraCS:gmPuQGAhUMZWIPSbKfbKMaYM:6cd95294da9fa7ce60990d87f36ea2c917ff8fb38dc4599b6d9d1173f5405953'

ENDPOINT = ""  # Use endpoint name if defined in flow settings, else fallback to FLOW_ID

# Default tweaks (can be customized if needed)
TWEAKS = {
    "ChatInput-n63ev": {},
    "ChatOutput-IJlVz": {},
    "File-ciN11": {},
    "SplitText-ATIis": {},
    "AstraDB-mHggC": {},
    "Google Generative AI Embeddings-jhHuX": {},
    "Google Generative AI Embeddings-J6MVt": {},
    "GoogleGenerativeAIModel-qj4sw": {},
    "AstraDB-63lqj": {},
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
        "output_type": "chat",  # Adjust based on your flow's input/output type
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


# Streamlit UI
st.title("LangFlow + AstraDB Deployment")

# Input box for user message
message = st.text_input("Enter your message", placeholder="Type your query here...")

# Button to trigger the LangFlow execution
if st.button("Run Flow"):
    if not message.strip():
        st.error("Please enter a valid message.")
    else:
        with st.spinner("Running the flow..."):
            result = run_flow(message)
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            extracted_text = result['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        # Display the extracted text in Streamlit
            st.text("Output:")
            st.text(extracted_text) # Display the JSON response

