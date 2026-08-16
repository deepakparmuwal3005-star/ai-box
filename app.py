import streamlit as st
from google import genai
import requests
import json
import html

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Product Intelligence",
    page_icon="🛍️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: #0b1020;
    color: white;
}

.hero {
    padding: 35px 20px;
    border-radius: 25px;
    background: linear-gradient(
        135deg,
        #111936,
        #18234d,
        #10182f
    );
    text-align: center;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.08);
}

.hero h1 {
    font-size: 45px;
    margin-bottom: 5px;
}

.hero p {
    color: #b8c1d9;
    font-size: 17px;
}

.search-box {
    background: #121a31;
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

.product-card {
    background: #121a31;
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}

.product-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 10px;
}

.price {
    font-size: 25px;
    font-weight: 800;
    color: #66e3a5;
}

.rating {
    color: #ffd166;
    font-weight: 700;
}

.info-box {
    background: #121a31;
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

.badge {
    display: inline-block;
    background: #222d50;
    padding: 7px 12px;
    border-radius: 20px;
    margin: 4px;
    color: #dbe4ff;
}

.ai-box {
    background: linear-gradient(
        135deg,
        #151f42,
        #10182f
    );
    padding: 25px;
    border-radius: 22px;
    border: 1px solid rgba(100,150,255,0.18);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>🛍️ AI Product Intelligence</h1>
    <p>
        Search any product and get price, image, rating,
        reviews and an AI-powered SEO description.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Settings")

gemini_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    help="Enter your Google Gemini API key."
)

serpapi_key = st.sidebar.text_input(
    "SerpApi Key",
    type="password",
    help="Used for Google Shopping product information."
)

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 Gemini generates the AI content. "
    "SerpApi finds shopping information such as price, "
    "rating, reviews and product images."
)

# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.markdown('<div class="search-box">', unsafe_allow_html=True)

product_query = st.text_input(
    "🔎 Search Product",
    placeholder="Example: Nike Air Jordan 1 Retro"
)

country = st.selectbox(
    "🌍 Market",
    ["India", "United States", "United Kingdom", "Canada", "Australia"]
)

search_button = st.button(
    "🔍 Find Product",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SERPAPI SEARCH
# --------------------------------------------------

def search_products(query, api_key, market):

    locations = {
        "India": "India",
        "United States": "United States",
        "United Kingdom": "United Kingdom",
        "Canada": "Canada",
        "Australia": "Australia"
    }

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": api_key,
        "location": locations[market],
        "hl": "en",
        "gl": "in" if market == "India" else "us"
    }

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"SerpApi error: {response.status_code}"
        )

    data = response.json()

    return data.get("shopping_results", [])


# --------------------------------------------------
# GEMINI DESCRIPTION
# --------------------------------------------------

def generate_ai_content(product, gemini_api_key):

    client = genai.Client(
        api_key=gemini_api_key
    )

    title = product.get("title", "")
    price = product.get("price", "Not available")
    rating = product.get("rating", "Not available")
    reviews = product.get("reviews", "Not available")
    source = product.get("source", "Not available")
    snippet = product.get("snippet", "")

    prompt = f"""
You are an expert e-commerce SEO copywriter.

Create product content using ONLY the information provided below.

PRODUCT:
{title}

PRICE:
{price}

RATING:
{rating}

REVIEWS:
{reviews}

SELLER:
{source}

AVAILABLE DESCRIPTION:
{snippet}

IMPORTANT:
- Do not invent technical specifications.
- Do not invent warranty information.
- Do not invent manufacturing information.
- If manufacturer/brand is not clearly available, say "Not listed".
- Keep facts accurate.
- Make the description attractive and SEO-friendly.

Return ONLY valid JSON in this structure:

{{
    "brand": "",
    "manufacturer": "",
    "category": "",
    "short_description": "",
    "full_description": "",
    "key_highlights": [
        "",
        "",
        "",
        ""
    ],
    "seo_keywords": [
        "",
        "",
        "",
        "",
        ""
    ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown JSON fences if Gemini returns them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)


# --------------------------------------------------
# SEARCH ACTION
# --------------------------------------------------

if search_button:

    if not product_query:
        st.warning("Please enter a product name.")

    elif not serpapi_key:
        st.warning(
            "⚠️ SerpApi API Key enter karo. "
            "Isse product image, price, rating aur shopping data milega."
        )

    elif not gemini_key:
        st.warning(
            "⚠️ Gemini API Key enter karo."
        )

    else:

        try:

            with st.spinner(
                "🔎 Google Shopping se products search ho rahe hain..."
            ):

                products = search_products(
                    product_query,
                    serpapi_key,
                    country
                )

            if not products:

                st.error(
                    "Product nahi mila. Product ka naam thoda specific try karo."
                )

            else:

                st.session_state["products"] = products
                st.session_state["searched"] = True

        except Exception as e:

            st.error("Product search mein error aaya.")
            st.code(str(e))


# --------------------------------------------------
# PRODUCT RESULTS
# --------------------------------------------------

if st.session_state.get("searched", False):

    products = st.session_state["products"]

    st.markdown("## 🛍️ Products Found")

    st.caption(
        f"{len(products)} shopping results found for "
        f"**{product_query}**"
    )

    # Show first 6 products
    display_products = products[:6]

    cols = st.columns(3)

    for index, product in enumerate(display_products):

        with cols[index % 3]:

            image = product.get("thumbnail")
            title = product.get(
                "title",
                "Product"
            )

            price = product.get(
                "price",
                "Price unavailable"
            )

            rating = product.get(
                "rating",
                "N/A"
            )

            reviews = product.get(
                "reviews",
                0
            )

            source = product.get(
                "source",
                "Unknown seller"
            )

            link = product.get(
                "product_link",
                product.get("link", "")
            )

            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )

            if image:
                st.image(
                    image,
                    use_container_width=True
                )

            st.markdown(
                f'<div class="product-title">{html.escape(title[:90])}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="price">{html.escape(str(price))}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="rating">⭐ {rating} '
                f'| {reviews} reviews</div>',
                unsafe_allow_html=True
            )

            st.caption(
                f"🏪 {source}"
            )

            if link:

                st.link_button(
                    "🛒 View Product",
                    link,
                    use_container_width=True
                )

            if st.button(
                "✨ Generate AI Details",
                key=f"select_{index}",
                use_container_width=True
            ):

                st.session_state["selected_product"] = product

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# --------------------------------------------------
# SELECTED PRODUCT
# --------------------------------------------------

if "selected_product" in st.session_state:

    product = st.session_state["selected_product"]

    st.markdown("---")

    st.markdown(
        "## ✨ Selected Product"
    )

    col1, col2 = st.columns([1, 1.5])

    with col1:

        image = product.get("thumbnail")

        if image:
            st.image(
                image,
                use_container_width=True
            )

    with col2:

        title = product.get(
            "title",
            "Product"
        )

        st.markdown(
            f"# {title}"
        )

        st.markdown(
            f"### 💰 {product.get('price', 'Not available')}"
        )

        st.markdown(
            f"### ⭐ {product.get('rating', 'N/A')} / 5"
        )

        st.write(
            f"👥 {product.get('reviews', 'N/A')} reviews"
        )

        st.write(
            f"🏪 Seller: {product.get('source', 'Not available')}"
        )

        delivery = product.get(
            "delivery",
            "Information not available"
        )

        st.write(
            f"🚚 Delivery: {delivery}"
        )

        if product.get("product_link"):

            st.link_button(
                "🛒 Buy / View Product",
                product["product_link"]
            )


# --------------------------------------------------
# AI DETAILS BUTTON
# --------------------------------------------------

if "selected_product" in st.session_state:

    st.markdown("---")

    generate_button = st.button(
        "🚀 Generate Complete AI Product Details",
        use_container_width=True
    )

    if generate_button:

        try:

            with st.spinner(
                "🤖 Gemini AI product details generate kar raha hai..."
            ):

                ai_data = generate_ai_content(
                    st.session_state["selected_product"],
                    gemini_key
                )

            st.session_state["ai_data"] = ai_data

        except Exception as e:

            st.error(
                "AI generation mein error aaya."
            )

            st.code(str(e))


# --------------------------------------------------
# AI OUTPUT
# --------------------------------------------------

if "ai_data" in st.session_state:

    data = st.session_state["ai_data"]

    st.markdown("---")

    st.markdown(
        '<div class="ai-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🤖 AI Product Intelligence"
    )

    # Basic information

    st.markdown("### 🏷️ Product Information")

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric(
            "Brand",
            data.get("brand", "Not listed")
        )

    with info2:
        st.metric(
            "Manufacturer",
            data.get(
                "manufacturer",
                "Not listed"
            )
        )

    with info3:
        st.metric(
            "Category",
            data.get(
                "category",
                "Not listed"
            )
        )

    st.markdown("---")

    # Short description

    st.markdown("### 📝 Short Description")

    st.write(
        data.get(
            "short_description",
            ""
        )
    )

    # Full description

    st.markdown(
        "### 📖 SEO Product Description"
    )

    full_description = data.get(
        "full_description",
        ""
    )

    st.write(full_description)

    # Highlights

    st.markdown(
        "### ⭐ Key Highlights"
    )

    highlights = data.get(
        "key_highlights",
        []
    )

    for item in highlights:
        st.markdown(
            f"• {item}"
        )

    # Keywords

    st.markdown(
        "### 🔍 SEO Keywords"
    )

    keywords = data.get(
        "seo_keywords",
        []
    )

    for keyword in keywords:

        st.markdown(
            f'<span class="badge">#{html.escape(keyword)}</span>',
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # Download

    download_text = f"""
PRODUCT DESCRIPTION

{full_description}

KEY HIGHLIGHTS
{chr(10).join("- " + x for x in highlights)}

SEO KEYWORDS
{", ".join(keywords)}
"""

    st.download_button(
        "⬇️ Download Description",
        download_text,
        file_name="product_description.txt",
        mime="text/plain",
        use_container_width=True
    )
