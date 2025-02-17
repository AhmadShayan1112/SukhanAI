import streamlit as st
import load
#import load  # Ensure load.py contains the user_input function

def main():
    st.set_page_config(page_title="SukhanAI - Roman Urdu Poetry Generator", layout="centered", initial_sidebar_state="expanded")
    
    # Custom CSS for enhanced dark theme
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: #121212;
            color: #E0E0E0;
            font-family: 'Arial', sans-serif;
        }
        .stTextInput input, .stNumberInput input {
            background-color: #1E1E1E;
            color: #E0E0E0;
            border-radius: 8px;
            border: 1px solid #333;
            padding: 10px;
        }
        .stButton>button {
            background-color: #FF5733;
            color: white;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            padding: 12px 24px;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #C70039;
        }
        .stMarkdown h1 {
            color: #FFCC00;
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
        }
        .stMarkdown{
            color: #FF5733;
        }
        .stMarkdown h2 {
            color: #FFCC00;
            text-align: center;
            font-size: 28px;
            margin-top: 20px;
        }
        .generated-text {
            font-size: 22px;
            color: #FFD700;
            font-family: 'Georgia', serif;
            text-align: center;
            background-color: #222;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .sidebar .sidebar-content {
            background-color: #1E1E1E;
            color: #E0E0E0;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: #888;
        }
        div[data-testid="stTextInput"] label, 
        div[data-testid="stNumberInput"] label {
        color: white !important;
        font-size: 20px !important; 
        font-weight: bold !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Sidebar for additional options or information
    with st.sidebar:
        st.markdown("## About SukhanAI")
        st.markdown("SukhanAI is an advanced Roman Urdu Poetry Generator that uses AI to create beautiful poetry based on your input.")
        st.markdown("### How to Use")
        st.markdown("1. Enter your input text in the text box.")
        st.markdown("2. Specify the number of lines you want to generate.")
        st.markdown("3. Click the 'Generate Poetry' button.")
        st.markdown("### Tips")
        st.markdown("- Use meaningful phrases or words for better results.")
        st.markdown("- Experiment with different line counts to see varied outputs.")
    
    st.markdown("# ✨ SukhanAI - Roman Urdu Poetry Generator ✨", unsafe_allow_html=True)
    
    user_data = st.text_input("✍️ Please Input The Data:")
    num_lines = st.number_input("📜 Please Enter The Number of Lines to Generate:", min_value=1, step=1, value=1)
    
    if st.button("🎶 Generate Poetry 🎶"):
        if user_data.strip():
            with st.spinner('Generating poetry...'):
                import time
                time.sleep(2)
                print(user_data)
                generated_poetry = load.user_input(user_data, num_lines)
                generated_poetry = "This is a sample generated poetry line.\nAnother line of poetry."
                formatted_poetry = generated_poetry.replace("\n", "<br>")
                st.markdown("## 🌟 Generated Poetry 🌟")
                st.markdown(f"<p class='generated-text'>{formatted_poetry}</p>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter some input text to generate poetry.")
    
    # Footer
    st.markdown("<div class='footer'>Made with ❤️ by SukhanAI | © 2025</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
