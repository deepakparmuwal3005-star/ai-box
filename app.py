import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="AI E-commerce Assistant", page_icon="🛍️", layout="centered")

st.title("🛍️ AI Product Description & SEO Generator")
st.markdown("Ek click mein apne product ke liye professional description aur SEO tags taiyar karein!")

# Sidebar API Key Input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Apni Gemini API Key yahan dalein", type="password")

if not api_key:
    st.warning("⚠️ Kripya pehle sidebar mein apni Gemini API Key darj karein.")
else:
    product_name = st.text_input("Product ka Naam (e.g., Wireless Gaming Mouse)")
    product_features = st.text_area("Product ke Features (e.g., RGB light, 5000 DPI, Bluetooth)")
    tone = st.selectbox("Tone chunein", ["Professional", "Exciting & Catchy", "Minimalist"])

    if st.button("Generate Content 🚀"):
        if product_name and product_features:
            with st.spinner("AI content likh raha hai..."):
                try:
                    # Configure Gemini
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"""
                    Aap ek expert E-commerce Copywriter aur SEO specialist hain.
                    Product Name: {product_name}
                    Key Features: {product_features}
                    Tone: {tone}

                    Format required:
                    1. Catchy Product Description
                    2. 5 Bullet Points (Key highlights)
                    3. SEO Meta Title aur Meta Description
                    4. 5 High-ranking Keywords
                    """

                    response = model.generate_content(prompt)

                    st.success("✨ Content taiyar hai!")
                    st.markdown("---")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Error aaya: {e}")
        else:
            st.warning("Kripya dono boxes (Name aur Features) bharein.")
