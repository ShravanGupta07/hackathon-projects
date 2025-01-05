import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Details
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "ff82a051-448c-4fae-8cbf-a564e6d27d96"
FLOW_ID = "4dba20be-13ec-42f0-aaa2-a9765561043a"
APPLICATION_TOKEN = "AstraCS:PDdMCqqoNrgPuKDksTfTBieZ:d319d99c2ee43ebf9e5e792ba72dc576d9c96840593f0150a5b837bfec1bf2b9"
ENDPOINT = ""  # Leave empty if no specific endpoint is needed

# Function to run the flow
def run_flow(message: str) -> dict:
    # Ensure the endpoint is set
    endpoint_to_use = ENDPOINT if ENDPOINT else FLOW_ID

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint_to_use}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {
        "Authorization": "Bearer " + APPLICATION_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    return {}

# Main function
def main():
    st.set_page_config(page_title="Social Media Insights", page_icon="📊", layout="wide")

    st.title("Social Media Performance Analysis")
    st.markdown("<h3 style='text-align: center;'>Get insights into your social media performance!</h3>", unsafe_allow_html=True)

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Input field for the user
    message = st.text_area("", placeholder="Ask me anything about your social media performance...", key="input_message", height=100)

    # Button to send the query
    if st.button("Generate Insights"):
        if not message.strip():
            st.error("Please enter a message")
            return

        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
                if response:
                    response_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "No response text found")

                    # Append user message and response to chat history
                    st.session_state["messages"].append({"user": message, "InsightBot": response_text})
                else:
                    st.error("No valid response received from the API.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state["messages"]:
        # User message
        st.markdown(f"**You:** {chat['user']}")
        
        # Bot response
        st.markdown(f"**InsightBot:** {chat['InsightBot']}")

        st.divider()  # Adds a divider for better readability

if __name__ == "__main__":
    main()
