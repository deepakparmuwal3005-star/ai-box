import google.generativeai as genai
import streamlit as st

st.title("AI Product Description Generator 🚀")

# Sidebar for API Key
api_key = st.sidebar.text_input(
    "Apni Gemini API Key yahan dalein", type="password"
)

if api_key:
  genai.configure(api_key=api_key)

  # User inputs
  product_name = st.text_input("Product ka Naam (e.g., Gaming Mouse)")
  product_features = st.text_area(
      "Features (e.g., RGB light, 5000 DPI, Bluetooth)"
  )
  tone = st.selectbox(
      "Tone chunein", ["Professional", "Casual", "Excited", "Persuasive"]
  )

  if st.button("Generate Content 🚀"):
    if product_name and product_features:
      try:
        # Automatically find a working model
        working_model = "gemini-1.5-flash"
        for m in genai.list_models():
          if "generateContent" in m.supported_generation_methods:
            if "flash" in m.name or "pro" in m.name:
              working_model = m.name
              break

        model = genai.GenerativeModel(working_model)

        prompt = (
            f"Write a {tone} product description for {product_name} with these"
            f" features: {product_features}"
        )

        with st.spinner("Generating..."):
          response = model.generate_content(prompt)
          st.success("Yeh raha aapka description:")
          st.write(response.text)

      except Exception as e:
        st.error(f"Error aaya: {e}")
    else:
      st.warning("Kripya sabhi fields bharein!")
else:
  st.info(
      "Kripya pehle sidebar mein apni Gemini API Key enter karein (Yeh secure"
      " hai)."
  )
