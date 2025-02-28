import google.generativeai as genai
import os



# Configure the API key
#GEMINIAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINIAI_API_KEY)

# Define generation configuration parameters
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model with the configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a new chat session and store history
chat_session = model.start_chat(history=[])

def chat_with_gemini(message, dom_content):
    """
    Send a message and DOM content to the Gemini chat model to receive a response.

    Args:
        message (str): The input message or prompt from the user.
        dom_content (str): The extracted DOM content to be parsed.

    Returns:
        str: The model's response text.
    """
    # Combine DOM content with the user's message as context
    full_message = f"Content to parse:\n\n{dom_content}\n\nUser query: {message}"
    response = chat_session.send_message(full_message)
    return response.text


def parse_with_gemini(parse_description):
    genai.configure(api_key=GEMINIAI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Request structured JSON from Gemini
    response = model.generate_content(
        parse_description
    )
    return response
