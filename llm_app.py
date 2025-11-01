# 1. Necessary Imports for Streamlit and Gemini
import os
import streamlit as st
from google import genai
from google.genai import types 

# --- Configuration ---
# 1. Set the page configuration for a beautiful UI
st.set_page_config(page_title="LLM Behavior Control Demo", layout="wide")

# 2. Setup Gemini API Client (Fetches key from environment variable)
# The key is expected to be set as: $env:GEMINI_API_KEY="YOUR_KEY" in the terminal
try:
    client = genai.Client() 
except Exception as e:
    st.error("❌ Error: GEMINI_API_KEY environment variable not set correctly.")
    st.info("Please set the environment variable in your terminal before running Streamlit.")
    st.stop() 

# 3. Core Function to Talk to the LLM
# We use st.cache_data to prevent unnecessary API calls when slider/context is not changed
@st.cache_data(show_spinner=False)
def generate_response(system_context, user_prompt, temperature_val):
    """Generates a response using the specified context, prompt, and parameters with Gemini."""
    
    # --- Prompt and Generation Parameters ---
    config = types.GenerateContentConfig(
        system_instruction=system_context,
        temperature=temperature_val,
        top_p=1.0 # Fixed Top-p for simplicity in this demo
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=config
        )
        return response.text
        
    except Exception as e:
        return f"An API error occurred: {e}"

# 4. Streamlit UI Design (Main Application Logic)
st.title("🧠 LLM Behavior Control: Prompt, Context, and Temperature Demo")
st.markdown("---")

# 5. Sidebar for Context and Temperature Control (Control Engineering)
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    # Context Engineering Input
    st.subheader("1. Context Engineering (Model Persona)")
    
    # --- CONTEXT CORRECTED AND EXPANDED FOR BUS CONTRAST ---
    context_value = (
        "Aap Karachi ki awaam ki taraf se E-Challan system par ek dilchasp aur do-rukhi (two-sided) ray dene waale hain. "
        "Aapka lehja mazahiyya (humorous) aur thoda sa exaggerate (exaggerated) hoga. "
        "Aapko zaroor batana hai ke **Green Line aur Red Bus** khush hain, lekin **local transport buses** ab mushkil mein hain. "
        "Aur un 'sad' teenagers ka zikar zaroor karna hai jinke mehange challan ab ghar jaa rahe hain, aur unhe apne walid (father) se maar pad sakti hai."
    )
    
    context_input = st.text_area(
        "Set the System's Role:",
        value=context_value,
        height=200 # Increased height for better view
    )
    
    # Temperature Parameter Control
    st.subheader("2. Temperature Parameter (Creativity)")
    temperature_input = st.slider(
        "Adjust Creativity (Temperature):",
        min_value=0.0,
        max_value=1.0,
        value=0.7, # Default to a balanced value
        step=0.05,
        help="Lower T (0.0-0.3) = Factual/Predictable. Higher T (0.8-1.0) = Creative/Random."
    )
    
    st.info(f"Current Temperature: **{temperature_input}**")
    
# 6. Main Chat Area for Prompt and Output
st.header("💬 Prompt and Output")

# --- PLACEHOLDER CORRECTED ---
# The previous placeholder had incorrect syntax (e.g.="...")
user_prompt = st.text_input(
    "Ask your question (Prompt Engineering):",
    placeholder="Karachi E-Challan system par public ke radd-e-amal (reaction) ka ek mazahiyya jaiza (review) pesh karien.",
    key="prompt_input"
)

# 7. Response Generation
if user_prompt:
    with st.spinner("Generating response..."):
        # Call the generation function with user-defined controls
        final_response = generate_response(
            system_context=context_input,
            user_prompt=user_prompt,
            temperature_val=temperature_input
        )
        
        # Display the result
        st.subheader("LLM Response:")
        st.markdown(final_response)
        st.markdown("---")
        st.caption(f"**Parameters Used:** System Context Set, Temperature={temperature_input}")