from openai import OpenAI
import streamlit as st
import base64
from io import BytesIO

with st.sidebar:
    user_openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
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
def transcribe_image(base64_image, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    context = open('context.txt', 'r').read()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": context,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content
    transcription = response['data'][0]['text']
    return transcription

# Display a button to trigger transcription
if uploaded_file is not None:
    image_base64 = encode_image(uploaded_file)

    # Transcribe Button
    if st.button("Transcribe Image"):
        if user_openai_api_key == "":
            st.error("Please enter your OpenAI API key")
        else:
            st.spinner("Transcribing the document...")
            try:
                transcript = transcribe_image(image_base64, user_openai_api_key)
                st.write("Transcription:")
                st.text_area("Transcribed Text", transcript, height=300)
            except Exception as e:
                st.error(f"Error: {e}")
