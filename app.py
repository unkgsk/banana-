# pip install transformers Pillow torch streamlit into the shell

import os
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from PIL import Image
import torch

# === Set up Hugging Face Token ===
os.environ["HF_TOKEN"] = "HF_TOKEN"  # Demo token for workshop

st.title("🍌 Recipe Image Captioning & QA")

# Add custom CSS for yellow background with banana images and black font color
st.markdown(
    """
    <style>
        body {
            background-color: #fff700;
            color: #000000;
        }
        .stApp {
            background-color: #fff700;
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg');
            background-repeat: repeat;
            background-size: 120px 80px;
            color: #000000;
        }
        .stMarkdown, .stText, .stTitle, .stInfo, .stSuccess, .stButton, .stFileUploader {
            color: #000000 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# === Image Upload ===
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # === BLIP Caption Generation ===
    st.write("Generating caption...")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)

    st.success("📝 Caption generated by BLIP model:")
    st.write(caption)

    # === QA Pipeline ===
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

    # Button for each question
    if st.button("What are the ingredients?"):
        result = qa_pipeline(question="What are the ingredients?", context=caption)
        st.info(f"Ingredients: {result['answer']}")

    if st.button("What are the cooking actions?"):
        result = qa_pipeline(question="What are the cooking actions?", context=caption)
        st.info(f"Cooking Actions: {result['answer']}")
else:
    st.info("Please upload an image to get started.")
