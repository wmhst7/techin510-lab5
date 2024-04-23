import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import time

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("API_KEY")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Streamlit app setup
st.title("Workout Planner")

# Initialize chat session if not already done
if "chat_session" not in st.session_state:
    st.session_state.chat_session = chat
    st.session_state.messages = []

# Ask for user information
with st.form("user_info"):
    st.write("Please enter your details:")
    age = st.number_input("Age", min_value=13, max_value=100, step=1)
    weight = st.number_input("Weight (in kg)", min_value=30, max_value=200, step=1)
    height = st.number_input("Height (in cm)", min_value=100, max_value=250, step=1)
    available_time = st.slider("How much time can you spend on workouts per week (hours)?", 0, 20, 3)
    goals = st.text_area("What are your fitness goals?")
    submit_button = st.form_submit_button("Generate Workout Plan")

if submit_button:
    user_details = f"Age: {age}, Weight: {weight} kg, Height: {height} cm, Available Time: {available_time} hours per week, Goals: {goals}"
    st.session_state.messages.append({"role": "user", "content": user_details})

    # Display user details and prepare the query
    query = f"Generate a weekly workout plan for someone with these details: {user_details}"

    # Simulate typing effect and show a loading spinner while waiting for response
    with st.spinner('AI is generating your personalized workout plan...'):
        response = st.session_state.chat_session.send_message(query)
        workout_plan = response.text  # Assuming response.text contains the string response
    
    # Display the generated workout plan
    st.session_state.messages.append({"role": "assistant", "content": workout_plan})
    with st.chat_message("assistant"):
        st.markdown(workout_plan)

