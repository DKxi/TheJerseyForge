import streamlit as st
import time

st.set_page_config(page_title="The Jersey Forge", layout="wide")

# ---------- PAGE STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "cart" not in st.session_state:
    st.session_state.cart = {}

# NEW: track if terms were accepted this session
if "terms_accepted" not in st.session_state:
    st.session_state.terms_accepted = False

# ---------- NAVIGATION FUNCTIONS ----------
def go_to_terms():
    st.session_state.page = "terms"

def go_to_cart():
    st.session_state.page = "cart"

def go_home():
    st.session_state.page = "home"


# ---------- BASIC STYLING ----------
st.markdown(
    """
    <style>
body {
    font-family: Arial, sans-serif;
    background: linear-gradient(#f7f3e9, #f0e4d0);
    cursor: url('https://cur.cursors-4u.net/sports/spo-1/spo16.cur'), auto;
}

/* PRODUCT BOX */
.product-box {
    border-radius: 14px;
    padding: 4px;
    margin-bottom: 12px;
    background: white;
    height: 2in;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: transform .25s ease, box-shadow .25s ease;
    overflow: hidden;
}

.product-box:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 18px rgba(0,0,0,0.25);
}

/* FADE-OUT for Added! */
.added-message {
    animation: fadeOut 1.2s forwards;
}

@keyframes fadeOut {
    0% { opacity: 1; }
    70% { opacity: 1; }
    100% { opacity: 0; }
}

/* COMING SOON LABEL */
.coming-soon-label {
    display: inline-block;
    padding: 4px 8px;
    background-color: #ff9800;
    color: white;
    border-radius: 6px;
    font-size: 0.8rem;
    margin-top: 8px;
}

/* PRICE TAG */
.price-tag {
    font-weight: bold;
    color: #2e7d32;
    font-size: 1.1rem;
}

/* HEADER — BASKETBALL COURT */
.header-banner {
    background: linear-gradient(90deg, #d9a86c, #c68c53, #d9a86c);
    color: white;
    padding: 32px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    border: 4px solid #8b5a2b;
    box-shadow: 0 0 25px rgba(255, 165, 0, 0.6);
}

.header-banner::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 4px;
    background: white;
    opacity: 0.7;
}

.header-banner::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 140px;
    height: 140px;
    border: 5px solid white;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.7;
}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- PRODUCT DATA ----------
products = [
    {"name": "Michael Jordan 1996-97 Chicago Bulls Hardwood Swingman Jersey - For ages 11-14", "price": 45, "column": 1, "coming_soon": False},
    {"name": "Men's Chicago Bulls Michael Jordan White 1997/98 Jersey - For ages 11-14", "price": 45, "column": 1, "coming_soon": False},
    {"name": "MICHAEL JORDAN Chicago Bulls 1997-98 Jersey - For ages 11-14", "price": 45, "column": 1, "coming_soon": False},

    {"name": "Dwyane Wade Miami Heat 2005/06 Hardwood Classics Player Jersey - Red - For ages 11-14", "price": 45, "column": 2, "coming_soon": True},
    {"name": "Cleveland Cavaliers LeBron James Navy Hardwood Classics Swingman Jersey - For ages 11-14", "price": 45, "column": 2, "coming_soon": True},
    {"name": "Cleveland Cavaliers Lebron James 2015-16 Hardwood Classics Swingman Player Navy Alternate Jersey - For ages 11-14", "price": 45, "column": 2, "coming_soon": True},

    {"name": "Los Angeles Lakers Kareem Abdul-Jabbar Road Swingman Jersey - Light Gold - For ages 11-14", "price": 45, "column": 3, "coming_soon": True},
    {"name": "Los Angeles Lakers Magic Johnson Swingman Jersey - For ages 11-14", "price": 45, "column": 3, "coming_soon": True},
    {"name": "Los Angeles Lakers Magic Johnson Swingman Jersey (Alt) - For ages 11-14", "price": 45, "column": 3, "coming_soon": True},
]

# ============================================================
# ======================= HOME PAGE ==========================
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        '<div class="header-banner"><h1>The Jersey Forge</h1>'
        '<p>Our jerseys for cheap, doesnt make your wallet weep.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Cart button: show terms only once per session
    if st.button("🛒 Cart"):
        if st.session_state.terms_accepted:
            st.session_state.page = "cart"
        else:
            st.session_state.page = "terms"

    search_query = st.text_input("", placeholder="Search Here", label_visibility="collapsed")
    st.write("🔍 Use the search bar above to filter jerseys by any word in the name.")

    def filter_products(query):
        if not query:
            return products
        q = query.strip().lower()
        return [p for p in products if q in p["name"].lower().split()]

    filtered_products = filter_products(search_query)

    col1, col2, col3 = st.columns(3)
    columns_map = {1: col1, 2: col2, 3: col3}

    for p in filtered_products:
        col = columns_map[p["column"]]
        with col:
            st.markdown('<div class="product-box">', unsafe_allow_html=True)

            # Show fading "Added!" message if triggered
            if st.session_state.get(f"added_{p['name']}"):
                st.markdown('<p class="added-message" style="color:green;font-weight:bold;">Added!</p>', unsafe_allow_html=True)

            st.markdown(f"**{p['name']}**")
            st.markdown(f'<span class="price-tag">$ {p["price"]}.00</span>', unsafe_allow_html=True)

            if p["coming_soon"]:
                st.markdown('<div class="coming-soon-label">COMING SOON</div>', unsafe_allow_html=True)
            else:
                add_key = f"add_{p['name']}"
                remove_key = f"remove_{p['name']}"

                cols_btn = st.columns(2)

                # ADD TO CART BUTTON (NO FLICKER)
                with cols_btn[0]:
                    if st.button("Add to Cart", key=add_key):
                        st.session_state.cart[p["name"]] = st.session_state.cart.get(p["name"], 0) + 1

                        # Trigger fade-out message
                        st.session_state[f"added_{p['name']}"] = True

                        st.rerun()

                # REMOVE BUTTON
                with cols_btn[1]:
                    if st.button("Remove", key=remove_key):
                        if p["name"] in st.session_state.cart:
                            st.session_state.cart[p["name"]] -= 1
                            if st.session_state.cart[p["name"]] <= 0:
                                del st.session_state.cart[p["name"]]

            st.markdown("</div>", unsafe_allow_html=True)

    # Clear all "Added!" flags after showing once
    for key in list(st.session_state.keys()):
        if key.startswith("added_"):
            del st.session_state[key]

# ============================================================
# ================= TERMS & CONDITIONS PAGE ==================
# ============================================================

elif st.session_state.page == "terms":

    st.title("Terms & Conditions – The Jersey Forge")

    st.write("""
    ### 1. Independent, Customized Products
    All jerseys sold by **The Jersey Forge** are fully modified and customized fan-made products. 
    They are **not** official merchandise and have **no affiliation** with the NBA or any team.

    ### 2. No Association with Original Brands
    These jerseys are artistic interpretations and **not replicas** of official products.

    ### 3. Waiver of Claims
    Customers agree they **cannot take legal action** against The Jersey Forge.

    ### 4. All Sales Final
    No returns. No refunds. All sales are final.

    ### 5. Acceptance
    By continuing, you agree to all terms above.
    """)

    # Accept terms once, then go to cart
    if st.button("I Agree — Go to Cart"):
        st.session_state.terms_accepted = True
        st.session_state.page = "cart"

    st.button("Back to Store", on_click=go_home)

# ============================================================
# ======================== CART PAGE =========================
# ============================================================

elif st.session_state.page == "cart":

    header_left, header_right = st.columns([3, 1])

    with header_left:
        st.markdown("<h2 style='margin-bottom:0;'>Shopping Cart</h2>", unsafe_allow_html=True)

    subtotal = 0
    total_items = sum(st.session_state.cart.values())
    for name, qty in st.session_state.cart.items():
        price = next(p["price"] for p in products if p["name"] == name)
        subtotal += price * qty

    with header_right:
        st.markdown(
            f"<p style='text-align:right; font-size:16px; margin-top:18px;'>"
            f"Subtotal ({total_items} items): <strong>${subtotal:.2f}</strong></p>",
            unsafe_allow_html=True
        )

    st.write("---")

    st.button("⬅ Back to Store", on_click=go_home)

    if not st.session_state.cart:
        st.write("Your cart is empty.")
        st.stop()

    for name, qty in st.session_state.cart.items():

        price = next(p["price"] for p in products if p["name"] == name)

        img_col, info_col, price_col = st.columns([1, 3, 1])

        with img_col:
            st.markdown(
                """
                <div style="
                    width:120px;
                    height:120px;
                    border:2px solid #ccc;
                    border-radius:8px;
                    background-color:#f5f5f5;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:12px;
                    color:#777;
                ">
                    Image Here
                </div>
                """,
                unsafe_allow_html=True
            )

        with info_col:
            st.markdown(f"**{name}**")
            st.write("Color: Custom")
            st.write("Size: Youth 11–14")
            st.write("In Stock")

            new_qty = st.number_input(
                f"Qty for {name}",
                min_value=1,
                max_value=10,
                value=qty,
                key=f"qty_{name}"
            )

            if new_qty != qty:
                st.session_state.cart[name] = new_qty

            colA, colB = st.columns(2)
            with colA:
                if st.button("Delete", key=f"del_{name}"):
                    del st.session_state.cart[name]
                    st.rerun()
            with colB:
                st.write("Save for later")

        with price_col:
            st.markdown(f"**${price:.2f}**")

        st.write("---")

    st.markdown(f"### Subtotal: **${subtotal:.2f}**")
