import os

import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO


# Disable PIL debug logging
# import logging
# logging.getLogger('PIL').setLevel(logging.WARNING)


# Suppress OpenMP warning
# os.environ['KMP_WARNINGS'] = '0'


# Configure app-specific logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

st.set_page_config(
    page_title="✂️ rmbg",
    layout="centered",
    initial_sidebar_state="collapsed",  # Faster initial load
)


def show_footer():
    st.markdown(
        """
    <div style='position: fixed; bottom: 0; left: 0; right: 0; width: 100%; text-align: center; background-color: transparent; padding: 10px;'>
        <hr style='margin: 0.5em auto; width: 90%; border-color: rgba(0, 0, 0, 0.1);'>
        <p style='color: #0066cc; margin: 0; font-size: 14px;'>
            Developed by <a href='https://github.com/krishangupta33' style='color: #0066cc; text-decoration: none; font-weight: bold;'>Krishan Gupta</a> | 
            <a href='https://github.com/krishangupta33/image_background-remover-docker-app' style='color: #0066cc; text-decoration: none; font-weight: bold;'>See the complete repo</a>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


# Preload the model in background
@st.cache_resource
def get_model():
    from rembg import new_session

    return new_session()


# Initialize model in background
model = get_model()

st.title("Remove Background from Images")


# Load and cache demo image
@st.cache_data
def load_demo_image():
    demo_image = Image.open("cat.webp")
    demo_output = remove(demo_image, session=model)
    return demo_image, demo_output


col1, col2 = st.columns(2)

# File uploader
uploaded_file = st.file_uploader(
    "Drop or select an image", type=["png", "jpg", "jpeg", "webp"]
)

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
        with st.spinner("Removing background... Please wait"):
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
        mime="image/png",
    )

else:
    # Show demo image
    demo_image, demo_output = load_demo_image()
    with col1:
        st.subheader("Example Input")
        st.image(demo_image, use_container_width=True)
    with col2:
        st.subheader("Example Output")
        st.image(demo_output, use_container_width=True)

    st.info("👆 Upload your own image to get started!")


with st.expander("ℹ️ About this app"):
    st.markdown(
        """
    This app removes backgrounds from images using the `rembg` library.
    - Supports PNG, JPG, JPEG, and WEBP formats
    - Free to use
    - No sign-up required
    - Your images are not stored
    """
    )

# Show footer
show_footer()
