import streamlit as st
import load  # Ensure load.py contains the user_input function

def main():
    st.title("SukhanAI - Roman Urdu Poetry Generator")
    
    # User input for data
    user_data = st.text_input("Please Input The Data:")
    num_lines = st.number_input("Please Enter The Number of Lines to Generate:", min_value=1, step=1, value=1)
    
    if st.button("Generate Poetry"):
        if user_data.strip():
            generated_poetry = load.user_input(user_data, num_lines)
            word=""
            for char in generated_poetry:
                if char == "\n":
                    st.write(word)  
                    word = ""
                else:
                      word += char 
        else:
            st.warning("Please enter some input text to generate poetry.")

if __name__ == "__main__":
    main()
