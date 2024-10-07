import streamlit as st
import openai
import time
from country_list import countries_for_language


# Set up OpenAI API key
openai.api_key = st.secrets["api_key"]
# Predefined credentials (for simplicity, these are hardcoded)
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]

countries = dict(countries_for_language('en'))

# Predefined options
countries = countries.values()#['United States', 'Canada', 'United Kingdom', 'Australia', 'India']  # You can add more countries here

def get_ai_response(question):
    # Use OpenAI's ChatCompletion method for chat-based models like GPT-4 and GPT-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or 'gpt-4' if you have access
        messages=[
            {"role": "system", "content": "You are a helpful accountant and you give detailed tax breakdown and also the percentage."},
            {"role": "user", "content": question}
        ],
        max_tokens=300,  # Increase max_tokens to allow for a longer response
        temperature=0.7  # You can set it to 0 for more focused responses
    )
    return response['choices'][0]['message']['content'].strip()

def display_typing_effect(response_text):
    # Split response into words instead of characters to prevent overflow
    words = response_text.split()
    displayed_text = ""
    
    for word in words:
        displayed_text += word + " "
        # Update the markdown with new text
        placeholder.markdown(displayed_text.strip())  # Use markdown for text wrapping
        time.sleep(0.1)  # Adjust delay for typing effect (by word)

# Check if user is authenticated
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def login():
    st.title("Login")
    
    # Use a form for username/password login to handle form submission properly
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password. Please try again.")

# If the user is not authenticated, show the login form
if not st.session_state.authenticated:
    login()
else:

    # Streamlit UI
    st.title("AI Tax Donation Question")
    st.write("Select your country of residence and the country you're donating to.")

    # Dropdown for residence (Option1)
    residence = st.selectbox("I live in:", countries, index=0)

    # Dropdown for donation destination (Option2)
    donation_destination = st.selectbox("I am donating money to:", countries, index=1)

    # Format the question
    question = f"I live in {residence} and I am donating money to {donation_destination}, would I get a tax break?"

    # Display the generated question
    st.write(f"Your Question: {question}")

    # When the user presses the 'Ask' button
    if st.button('Ask'):
        with st.spinner('Generating response...'):
            answer = get_ai_response(question)
        
        # Simulate typing effect in Streamlit
        st.success("AI's Response:")
        placeholder = st.empty()  # Create a placeholder for the typing effect
        
        # Gradually display the response text word by word
        display_typing_effect(answer)
        
        # After typing effect, display the full response
        #st.write("Full Response:")
        #st.text_area("AI's Complete Response", value=answer, height=200)  # You can adjust height as needed
