import os
# Disable PIL debug logging
import logging
logging.getLogger('PIL').setLevel(logging.WARNING)

# Suppress OpenMP warning
os.environ['KMP_WARNINGS'] = '0'

import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO

# Configure app-specific logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

st.set_page_config(
    page_title="✂️ rmbg",
    layout="centered",
    initial_sidebar_state="collapsed"  # Faster initial load
)

# Preload the model in background
@st.cache_resource
def get_model():
    from rembg import new_session
    return new_session()

# Initialize model in background
model = get_model()

st.title("Remove Background from Images")

# File uploader
uploaded_file = st.file_uploader("Drop or select an image", type=['png', 'jpg', 'jpeg', 'webp'])

if uploaded_file is not None:
    # Display the original image
    input_image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(input_image, use_container_width=True)
    
    with col2:
        st.subheader("Background Removed")
        # Add a spinner while processing
        with st.spinner('Removing background... Please wait'):
            # Process the image using cached model
            output_image = remove(input_image, session=model)
            st.image(output_image, use_container_width=True)
    
    # Convert the image to bytes for download
    buf = BytesIO()
    output_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    # Add download button
    st.download_button(
        label="Download processed image",
        data=byte_im,
        file_name="removed_bg.png",
        mime="image/png"
    )

    # Add developer attribution
    st.markdown("---")
    st.markdown("Developed by [Krishan Gupta](https://github.com/krishangupta33)")