import streamlit as st
from scrape import main, extract_body_content, clean_body_content
from ai import chat_with_gemini  # Import the updated chat function

# Streamlit UI
st.set_page_config(page_title="AstraScrape AI", page_icon=":robot_face:")  # Set the page title and icon
st.title("AstraScrape AI")  # Set the main title

st.header("AI Web Scraper & Chat")  # Add a header

url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        # Scrape the website content
        dom_content = main(url)
        if dom_content:
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the cleaned content in Streamlit session state
            st.session_state['dom_content'] = cleaned_content

            # Display the content in an expandable area
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.write("Failed to retrieve content from the website.")

# Step 2: Chat Interface
if 'dom_content' in st.session_state:
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []  # Initialize chat history

    user_message = st.text_input("Ask a question about the content")

    if st.button("Send"):
        if user_message:
            # Add user message to chat history
            st.session_state['chat_history'].append(("User", user_message))
            
            # Get response from Gemini, passing both the user message and DOM content
            response = chat_with_gemini(user_message, st.session_state['dom_content'])
            
            # Add Gemini's response to chat history
            st.session_state['chat_history'].append(("Gemini", response))

    # Display the chat history
    st.write("Chat History:")
    for sender, message in st.session_state['chat_history']:
        st.write(f"**{sender}:** {message}")
else:
    st.write("No DOM content to parse. Please scrape a website first.")
