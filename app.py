import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Product Description Generator",
    page_icon="🚀"
)

st.title("AI Product Description Generator 🚀")

# Sidebar
st.sidebar.header("Gemini API")

api_key = st.sidebar.text_input(
    "Apni Gemini API Key yahan dalein",
    type="password"
)

if api_key:

    try:
        # New Google GenAI SDK
        client = genai.Client(api_key=api_key)

        # Product inputs
        product_name = st.text_input(
            "Product ka Naam (e.g., Gaming Mouse)"
        )

        product_features = st.text_area(
            "Features (e.g., RGB light, 5000 DPI, Bluetooth)"
        )

        tone = st.selectbox(
            "Tone chunein",
            [
                "Professional",
                "Casual",
                "Excited",
                "Persuasive"
            ]
        )

        if st.button("Generate Content 🚀"):

            if product_name and product_features:

                prompt = f"""
Create a high-quality product description.

Product Name:
{product_name}

Product Features:
{product_features}

Tone:
{tone}

Requirements:
- Write an attractive product description
- Highlight the important features
- Make it easy to understand
- Make it suitable for an e-commerce website
- Do not make up specifications that were not provided
"""

                try:

                    with st.spinner("AI description generate kar raha hai..."):

                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=prompt
                        )

                    st.success("Description ready! 🚀")

                    st.markdown("### 📝 Product Description")

                    st.write(response.text)

                except Exception as e:

                    st.error("Gemini API mein error aa gaya.")

                    st.code(str(e))

            else:

                st.warning(
                    "Kripya Product Name aur Features dono bharein!"
                )

    except Exception as e:

        st.error("API Key ya Gemini connection mein problem hai.")

        st.code(str(e))

else:

    st.info(
        "👈 Pehle sidebar mein apni Gemini API Key enter karein."
    )
