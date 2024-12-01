import streamlit as st
import google.generativeai as genai
import random

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("AI Sales Competitor Simulation")
st.write("""
    This advanced simulation allows you to train by interacting with AI-driven competitors in different sales scenarios.
    Choose a sales scenario, customize your competitor's profile, and simulate a conversation for better sales training.
""")

# Scenario Selection
scenario = st.selectbox(
    "Select a Sales Scenario:",
    ["Negotiating Price", "Handling Objections", "Product Pitch", "Closing a Deal"]
)

# Competitor Profile Customization
competitor_style = st.selectbox(
    "Select Competitor Style:",
    ["Aggressive", "Passive", "Price-sensitive", "Value-driven"]
)

# Prompt input field for additional context or specifics
additional_context = st.text_input("Additional Context (optional):", "")

# Button to generate response
if st.button("Simulate Competitor Response"):
    try:
        # Prepare the prompt based on scenario and competitor style
        prompt = f"Sales Scenario: {scenario}\nCompetitor Style: {competitor_style}\n"
        if additional_context:
            prompt += f"Additional Context: {additional_context}\n"
        
        # Load and configure the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate multiple responses to show variability
        responses = []
        for _ in range(3):  # Generate 3 different responses
            response = model.generate_content(prompt)
            responses.append(response.text)
        
        # Randomly select a response to simulate variability in the competitor's approach
        selected_response = random.choice(responses)
        
        # Display the competitor's response
        st.write("Competitor's Response:")
        st.write(selected_response)
        
        # Sales Tips and Analysis
        st.write("\n### Sales Tips for this Scenario:")
        if "discount" in selected_response.lower():
            st.write("- Consider offering value before discussing discounts.")
            st.write("- Be careful with deep discounts; make sure to justify the value you're providing.")
        elif "objection" in selected_response.lower():
            st.write("- Address objections empathetically, and always steer the conversation back to value.")
            st.write("- Validate the customer's concern and offer a solution.")
        else:
            st.write("- Always highlight the benefits and value of your product before diving into price negotiations.")
            st.write("- Keep the conversation focused on how your solution can meet the customer's needs.")
        
        # Continue the conversation: simulate another round of dialogue
        follow_up = st.text_input("Your Response to Competitor (optional):")
        if follow_up:
            follow_up_prompt = f"Customer's Response: {follow_up}\nCompetitor Style: {competitor_style}\nSales Scenario: {scenario}\n"
            follow_up_response = model.generate_content(follow_up_prompt)
            st.write("Competitor's Follow-Up Response:")
            st.write(follow_up_response.text)
    
    except Exception as e:
        st.error(f"Error: {e}")
