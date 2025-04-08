
import streamlit as st
from chatbot_data import OptumChatbot  # Import the OptumChatbot class from data_loading.py
def main():
    st.set_page_config(
        page_title="Optum India Chatbot",
        page_icon="🏥",
        layout="wide"
    )
    
    # Set up the header
    st.image("https://www.optum.in/content/dam/optum3/optum/en/images/header/logo.png", width=200)
    st.title("Optum India Website Chatbot")
    st.markdown("Ask any question about Optum India's services, solutions, and more!")
    
    # Initialize session state
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = OptumChatbot()
        
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    
    # Sidebar for initialization
    with st.sidebar:
        st.header("Chatbot Controls")
        
        if st.button("Initialize Chatbot"):
            success = st.session_state.chatbot.initialize()
            if success:
                st.session_state.initialized = True
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I've successfully scraped Optum India's website! You can now ask me questions about their services, solutions, and more."
                })
                
        if st.session_state.initialized:
            st.success("Chatbot is initialized and ready!")
        else:
            st.warning("Please initialize the chatbot before asking questions.")
            
        st.markdown("---")
        st.markdown("""
        ### About This Chatbot
        
        This chatbot has been trained on content from Optum India's official website.
        It can provide information about:
        
        - Optum's services and solutions
        - Company information
        - Contact details
        - Career opportunities
        - And more!
        """)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know about Optum India?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            if not st.session_state.initialized:
                response = "Please initialize the chatbot first by clicking the 'Initialize Chatbot' button in the sidebar."
                st.warning(response)
            else:
                with st.spinner("Finding answer from Optum India website..."):
                    response = st.session_state.chatbot.answer_question(prompt)
                st.write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()