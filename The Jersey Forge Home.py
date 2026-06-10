import streamlit as st

st.set_page_config(page_title="The Jersey Forge", layout="wide")

# ---------- BASIC STYLING ----------
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    .product-box {
         
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 2in; /* ~2 inches spacing */
         
        
    }
    .coming-soon-label {
        display: inline-block;
        padding: 4px 8px;
        background-color: #ff9800;
        color: white;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-top: 8px;
    }
    .price-tag {
        font-weight: bold;
        color: #2e7d32;
        font-size: 1.1rem;
    }
    .header-banner {
        background: black;
        color: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    .cart-box {
        border: 2px solid #1976d2;
        border-radius: 10px;
        padding: 12px;
        background-color: #e3f2fd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SESSION STATE FOR CART ----------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ---------- PRODUCT DATA ----------
products = [
    # Column 1 – purchasable
    {
        "name": "Michael Jordan 1996-97 Chicago Bulls Hardwood Swingman Jersey - For ages 11-14",
        "price": 45,
        "column": 1,
        "coming_soon": False,
    },
    {
        "name": "Men's Chicago Bulls Michael Jordan White 1997/98 Jersey - For ages 11-14",
        "price": 45,
        "column": 1,
        "coming_soon": False,
    },
    {
        "name": "MICHAEL JORDAN Chicago Bulls 1997-98 Jersey - For ages 11-14",
        "price": 45,
        "column": 1,
        "coming_soon": False,
    },
    # Column 2 – coming soon
    {
        "name": "Dwyane Wade Miami Heat 2005/06 Hardwood Classics Player Jersey - Red - For ages 11-14",
        "price": 45,
        "column": 2,
        "coming_soon": True,
    },
    {
        "name": "Cleveland Cavaliers LeBron James Navy Hardwood Classics Swingman Jersey - For ages 11-14",
        "price": 45,
        "column": 2,
        "coming_soon": True,
    },
    {
        "name": "Cleveland Cavaliers Lebron James 2015-16 Hardwood Classics Swingman Player Navy Alternate Jersey - For ages 11-14",
        "price": 45,
        "column": 2,
        "coming_soon": True,
    },
    # Column 3 – coming soon
    {
        "name": "Los Angeles Lakers Kareem Abdul-Jabbar Road Swingman Jersey - Light Gold - For ages 11-14",
        "price": 45,
        "column": 3,
        "coming_soon": True,
    },
    {
        "name": "Los Angeles Lakers Magic Johnson Swingman Jersey - For ages 11-14",
        "price": 45,
        "column": 3,
        "coming_soon": True,
    },
    {
        "name": "Los Angeles Lakers Magic Johnson Swingman Jersey (Alt) - For ages 11-14",
        "price": 45,
        "column": 3,
        "coming_soon": True,
    },
]

# ---------- HEADER / DECORATIONS ----------
st.markdown(
    '<div class="header-banner"><h1>The Jersey Forge</h1>'
    '<p>Our jerseys for cheap, doesnt make your wallet weep.</p>'
    '</div>',
    unsafe_allow_html=True,
)

# ---------- SEARCH BAR ----------
search_query = st.text_input("",
                             placeholder="Search Here",
                             label_visibility="collapsed")
st.write("🔍 Use the search bar above to filter jerseys by any word in the name.")

def filter_products(query):
    if not query:
        return products
    q = query.strip().lower()
    filtered = []
    for p in products:
        words = p["name"].lower().split()
        if q in words:
            filtered.append(p)
    return filtered

filtered_products = filter_products(search_query)

# ---------- MAIN LAYOUT: 3 COLUMNS ----------
col1, col2, col3 = st.columns(3)

columns_map = {1: col1, 2: col2, 3: col3}

for p in filtered_products:
    col = columns_map[p["column"]]
    with col:
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        st.markdown(f"**{p['name']}**")
        st.markdown(f'<span class="price-tag">$ {p["price"]}.00</span>', unsafe_allow_html=True)

        if p["coming_soon"]:
            st.markdown('<div class="coming-soon-label">COMING SOON</div>', unsafe_allow_html=True)
        else:
            # Add / Remove buttons for cart
            add_key = f"add_{p['name']}"
            remove_key = f"remove_{p['name']}"

            cols_btn = st.columns(2)
            with cols_btn[0]:
                if st.button("Add to Cart", key=add_key):
                    st.session_state.cart[p["name"]] = st.session_state.cart.get(p["name"], 0) + 1
            with cols_btn[1]:
                if st.button("Remove", key=remove_key):
                    if p["name"] in st.session_state.cart:
                        st.session_state.cart[p["name"]] -= 1
                        if st.session_state.cart[p["name"]] <= 0:
                            del st.session_state.cart[p["name"]]

        st.markdown("</div>", unsafe_allow_html=True)

# ---------- CART DISPLAY (LIVE UPDATING) ----------
st.markdown("## Cart")
st.markdown('<div class="cart-box">', unsafe_allow_html=True)

if not st.session_state.cart:
    st.write("Your cart is empty.")
else:
    total = 0
    for name, qty in st.session_state.cart.items():
        price = next(p["price"] for p in products if p["name"] == name)
        line_total = price * qty
        total += line_total
        st.write(f"{name} — Qty: {qty} — Line Total: ${line_total:.2f}")
    st.write(f"**Cart Total: ${total:.2f}**")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- TERMS AND CONDITIONS ----------
st.markdown("## Terms and Conditions – The Jersey Forge")

terms_text = """
### 1. Independent, Customized Products

All jerseys sold by **The Jersey Forge** are fully modified and customized fan-made products. 
They are **not** official merchandise and have **no affiliation, sponsorship, endorsement, or approval** from the National Basketball Association (NBA), any NBA team, any player, or any official league or licensing body.

The colors, materials, design details, and overall construction of jerseys offered by The Jersey Forge are intentionally different from any official or original products. 
By purchasing from The Jersey Forge, customers acknowledge and agree that these items are unique, customized creations and **do not represent** official NBA or team products.

### 2. No Association with Original Brands or Rights Holders

Customers understand and agree that:
- The Jersey Forge does not claim any official relationship with the NBA, its teams, players, or licensors.
- The jerseys are artistic, customized interpretations and are not replicas of official products.
- Any player names, numbers, or team references are used purely in a descriptive, fan-oriented manner and do not imply endorsement or authorization.

By completing a purchase, customers confirm that they are fully aware of this lack of association and accept the products as customized, non-official items.

### 3. Waiver of Claims and Limitation of Liability

By purchasing from The Jersey Forge, customers agree that they **cannot take any legal action** against The Jersey Forge, its owners, employees, or affiliates regarding:
- Alleged confusion with official NBA or team merchandise;
- Differences in color, design, materials, or construction compared to any original products;
- Any perceived lack of similarity to official jerseys.

Customers expressly waive any claims, demands, or causes of action arising out of or related to:
- Trademark, copyright, or licensing issues concerning third parties;
- The customized nature of the products;
- The manner in which the jerseys are designed, produced, or presented.

### 4. All Sales Final – No Returns or Refunds

All sales made by **The Jersey Forge** are **final**.

- **No returns** are accepted under any circumstances.
- **No refunds** will be issued for any reason, including but not limited to sizing issues, color preferences, design expectations, or changes of mind.
- Customers are responsible for reviewing product descriptions and making informed purchasing decisions before completing checkout.

By placing an order, customers acknowledge and agree that they have read, understood, and accepted this **no returns, no refunds, all sales final** policy.

### 5. Acceptance of Terms

By using this site, adding items to the cart, and/or completing a purchase, customers confirm that:
- They have read and understood these Terms and Conditions;
- They accept that all products from The Jersey Forge are customized, non-official items with no relation to the NBA or original manufacturers;
- They waive any right to pursue legal action against The Jersey Forge related to the nature, origin, or customization of the products;
- They agree that all sales are final and that no returns or refunds will be provided.

If a customer does not agree to these Terms and Conditions, they must not proceed with any purchase from **The Jersey Forge**.
"""

st.markdown(terms_text)
