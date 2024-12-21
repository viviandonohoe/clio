import openai 
import streamlit as st
import base64
from io import BytesIO

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/viviandonohoe/clio.git)"

st.title("Clio")
st.caption("A document transcription service powered by OpenAI")

uploaded_file = st.file_uploader("Upload an image", type=("jpg", "jpeg", "png"))

# Function to encode the image to base64
def encode_image(image_file):
    img = BytesIO(image_file.read())
    return base64.b64encode(img.getvalue()).decode('utf-8')

# Function to handle transcription
def transcribe_image(image_base64):
    # Set the API key
    openai.api_key = openai_api_key

    # Create the image transcription request
    response = openai.Image.create(
        model="gpt-4",  # Make sure to use the correct model
        images=[{
            "image_data": f"data:image/jpeg;base64,{image_base64}"
        }],
        max_tokens=1500
    )

    # Extract the transcription result
    transcription = response['data'][0]['text']
    return transcription

# Display a button to trigger transcription
if uploaded_file is not None:
    image_base64 = encode_image(uploaded_file)

    # Transcribe Button
    if st.button("Transcribe Image"):
        st.spinner("Transcribing the document...")
        try:
            transcript = transcribe_image(image_base64)
            st.write("Transcription:")
            st.text_area("Transcribed Text", transcript, height=300)
        except Exception as e:
            st.error(f"Error: {e}")
