from PIL import Image
import streamlit as st
import qrcode
import numpy as np
import io

# ==============================
# STRONG VISIBLE GRAYSCALE MOTION BACKGROUND
# ==============================
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(circle at 30% 30%, #ffffff20, #000000 70%),
        radial-gradient(circle at 70% 70%, #44444440, #000000 70%),
        radial-gradient(circle at 50% 50%, #ff000020, #000000 80%),
        linear-gradient(135deg, #222222, #000000);
    background-size: 300% 300%;
    animation: motionBG 6s ease-in-out infinite;
}

@keyframes motionBG {
    0%   { background-position: 0% 0%; }
    25%  { background-position: 100% 0%; }
    50%  { background-position: 100% 100%; }
    75%  { background-position: 0% 100%; }
    100% { background-position: 0% 0%; }
}

/* Transparency */
[data-testid="stHeader"], [data-testid="stSidebar"] {
    background: transparent !important;
}
.block-container {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# CUSTOM TITLE
# ==============================
st.markdown("""
<style>
.clean-title {
    font-size: 4rem;
    font-weight: 900;
    color: #280000;
    letter-spacing: 2px;
    transform: scaleY(2.0);
    transform-origin: center;
    font-family: 'Impact', sans-serif;
}
</style>

<h1 class="clean-title">QR CODE GENERATOR</h1>
""", unsafe_allow_html=True)

st.markdown("### ***Rewrapped!***")

# ==============================
# URL INPUT
# ==============================
url = st.text_input("ENTER THE URL:")

# ==============================
# COLOR SELECTION
# ==============================
bg_colour = st.selectbox(
    "ENTER THE BACKGROUND COLOUR :",
    ["black","white","red","green","blue","yellow","orange","purple","violet"]
)

dots_colour = st.selectbox(
    "ENTER THE DOTS COLOUR :",
    ["black","white","red","green","blue","yellow","orange","purple","violet"]
)

# ==============================
# GENERATE QR BUTTON
# ==============================
if st.button("GENERATE IMAGE"):
    if not url.strip():
        st.warning("Please enter a URL first!")
    else:
        # QR generation
        qr = qrcode.QRCode(
    version=None,
    box_size=30,   # FIX: prevent huge image crash
    border=4,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
)

        qr.add_data(url)
        qr.make(fit=True)

        # GET RAW QR → convert to real PIL Image
        qr_img = qr.make_image(back_color=bg_colour, fill_color=dots_colour)
        try:
            pil_img = qr_img.get_image()
        except:
            pil_img = qr_img
        qr.make(fit=True)

        # If still not real PIL image → force convert using numpy
        if not isinstance(pil_img, Image.Image):
            pil_img = Image.fromarray(np.array(pil_img))

        img = pil_img.convert("RGB")   # final clean PIL image

        # Convert image -> bytes for download
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        st.success("YOUR QR CODE HAS BEEN GENERATED!")

        # Show QR
        st.image(img, caption="Generated QR Code", use_container_width=True)

        # Download button
        st.download_button(
            label="DOWNLOAD QR CODE",
            data=img_bytes,
            file_name="qrcode.png",
            mime="image/png"
        )
