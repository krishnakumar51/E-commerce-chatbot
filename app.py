import streamlit as st
from ecommbot.retrieval_generation import generation
from ecommbot.ingest import ingestdata
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ingest data and set up the generation chain
vstore = ingestdata("done")
chain = generation(vstore)

# Set page configuration
st.set_page_config(page_title="E-Commerce Chatbot", page_icon="🤖")

# Title and header
st.title("E-Commerce Chatbot")
st.header("Chat with our E-Commerce Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input: Placeholder where user will input their prompt
if prompt := st.chat_input("Ask me anything about our products"):
    # Add user message to session state
    user_msg = {"role": "user", "content": prompt}
    st.session_state["messages"].append(user_msg)

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Generate response
            response = chain.invoke(prompt)
            st.markdown(response)
            
            # Add assistant message to session state
            assistant_msg = {"role": "assistant", "content": response}
            st.session_state["messages"].append(assistant_msg)
