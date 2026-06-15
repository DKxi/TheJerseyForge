import streamlit as st
import time
import smtplib
from email.mime.text import MIMEText

# ---------------- EMAIL FUNCTION ----------------
def send_order_email(order_number, items):
    sender = "konerudivij@gmail.com"
    receiver = "konerudivij@gmail.com"
    password = "ualo rcqp ydgq tvcp"  # Your Gmail App Password

    body = f"New order received.\n\nOrder Number: {order_number}\n\nItems:\n"
    for item, qty in items.items():
        body += f"- {item} x{qty}\n"

    totalprice = sum(qty * 45 for qty in items.values())
    body += f"\n\nTotal Price: ${totalprice}"

    msg = MIMEText(body)
    msg["Subject"] = f"New Jersey Forge Order #{order_number}"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="The Jersey Forge", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "terms_accepted" not in st.session_state:
    st.session_state.terms_accepted = False

# ---------------- NAVIGATION ----------------
def go_to_terms():
    st.session_state.page = "terms"

def go_to_cart():
    st.session_state.page = "cart"

def go_home():
    st.session_state.page = "home"

# ---------------- GLOBAL STYLING ----------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #1e1e2f, #2a2a40, #1e1e2f);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
    font-family: 'Segoe UI', sans-serif;
}
/* CART BUTTON + BADGE */
.cart-container {
    position: relative;
    display: inline-block;
}

.cart-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: #ff6600;
    color: white;
    font-size: 13px;
    font-weight: bold;
    padding: 2px 7px;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(255, 120, 0, 0.8);
}


@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* HEADER */
.header-banner {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    border: 2px solid rgba(255,255,255,0.15);
    box-shadow: 0 0 25px rgba(255, 165, 0, 0.5);
}

.header-banner h1 {
    font-size: 48px;
    color: #ffcc66;
    text-shadow: 0 0 12px #ffcc66;
}

.header-banner p {
    font-size: 20px;
    color: #fff;
}

/* PRODUCT CARD */
.product-box {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 2px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    transition: transform .25s ease, box-shadow .25s ease;
    height: 2in;
}

.product-box:hover {
    transform: scale(1.04);
    box-shadow: 0 10px 28px rgba(255,255,255,0.25);
}

/* BUTTONS */
button[kind="secondary"] {
    background: linear-gradient(135deg, #ffcc66, #ff9933);
    color: black !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    font-weight: bold !important;
    transition: 0.2s ease;
}

button[kind="secondary"]:hover {
    transform: scale(1.05);
    box-shadow: 0 0 12px #ffcc66;
}

/* SUBMIT BUTTON */
.submit-btn {
    background: linear-gradient(135deg, #ff9933, #ff6600);
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: white;
    cursor: pointer;
    transition: 0.25s ease;
    box-shadow: 0 0 18px rgba(255, 120, 0, 0.6);
}

.submit-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 28px rgba(255, 120, 0, 1);
}

/* PRICE TAG */
.price-tag {
    font-weight: bold;
    color: #ffcc66;
    font-size: 1.2rem;
/* ADDED! message */
.added-message {
    color: #7CFC00;
    font-weight: bold;
    font-size: 18px;
    text-shadow: 0 0 8px #7CFC00;
    animation: fadeOut 1.2s forwards;
}

@keyframes fadeOut {
    0% { opacity: 1; transform: scale(1); }
    60% { opacity: 1; transform: scale(1.15); }
    100% { opacity: 0; transform: scale(1); }
}

</style>
""", unsafe_allow_html=True)

# ---------------- PRODUCT DATA ----------------
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
        '<p>Our jerseys for cheap, doesn’t make your wallet weep.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # 3 columns: left space, cart button, why us button
    # PERFECTLY ALIGNED BUTTON ROW
    col_left, col_cart, col_why = st.columns([7, 1, 1])

    with col_cart:
        total_items = sum(st.session_state.cart.values())

        st.markdown(
            f"""
            <div class="cart-container">
                <div class="cart-badge">{total_items}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.button(
            "🛒 Cart",
            key="cart_button_home",
            on_click=lambda: st.session_state.update(
                page="cart" if st.session_state.terms_accepted else "terms"
            )
        )

    with col_why:
        st.button(
            "Why Us",
            key="whyus_button",
            on_click=lambda: st.session_state.update(page="whyus")
        )

    search_query = st.text_input("", placeholder="Search Here", label_visibility="collapsed")

    def filter_products(query):
        if not query:
            return products
        q = query.strip().lower()
        return [p for p in products if q in p["name"].lower()]

    filtered_products = filter_products(search_query)

    col1, col2, col3 = st.columns(3)
    columns_map = {1: col1, 2: col2, 3: col3}

    for p in filtered_products:
        col = columns_map[p["column"]]
        with col:
            st.markdown('<div class="product-box">', unsafe_allow_html=True)

            st.markdown(f"**{p['name']}**")
            st.markdown(f'<span class="price-tag">$ {p["price"]}.00</span>', unsafe_allow_html=True)

            timestamp_key = f"added_timestamp_{p['name']}"
            if timestamp_key in st.session_state:
                if time.time() - st.session_state[timestamp_key] < 2:
                    st.markdown('<p class="added-message">Added!</p>', unsafe_allow_html=True)

            if p["coming_soon"]:
                st.markdown('<div style="color:#ff9933;font-weight:bold;">COMING SOON</div>', unsafe_allow_html=True)
            else:
                add_key = f"add_{p['name']}"
                remove_key = f"remove_{p['name']}"

                cols_btn = st.columns(2)

                with cols_btn[0]:
                    if st.button("Add", key=add_key):
                        st.session_state.cart[p["name"]] = st.session_state.cart.get(p["name"], 0) + 1
                        st.session_state[f"added_timestamp_{p['name']}"] = time.time()
                        st.rerun()

                with cols_btn[1]:
                    if st.button("Remove", key=remove_key):
                        if p["name"] in st.session_state.cart:
                            st.session_state.cart[p["name"]] -= 1
                            if st.session_state.cart[p["name"]] <= 0:
                                del st.session_state.cart[p["name"]]

            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ================= TERMS & CONDITIONS PAGE ==================
# ============================================================

elif st.session_state.page == "terms":

    st.title("Terms & Conditions – The Jersey Forge")

    st.write("""
    #### 1. Independent, Customized Products
    All jerseys sold by **The Jersey Forge** are fully modified and customized fan-made products. 
    They are **not** official merchandise and have **no affiliation** with the NBA, any NBA team, or any official brand.

    ### 2. No Association with Original Brands
    These jerseys are artistic interpretations and **not replicas** of official products. 
    Any references to player names, numbers, or teams are purely for descriptive purposes and do not imply endorsement or association.

    ### 3. Custom, Fan-Made Items
    Each jersey is a **custom, fan-made item** created from independently sourced materials. 
    Designs, colors, and styles are inspired by basketball culture but are not official team merchandise.

    ### 4. Waiver of Claims
    By purchasing from **The Jersey Forge**, you agree that you **cannot take legal action** against The Jersey Forge, its owners, or its creators 
    for any claims related to branding, likeness, or unofficial status of the products.

    ### 5. No Returns or Refunds
    All sales are **final**. Due to the custom nature of each jersey, we do **not** offer returns, exchanges, or refunds, 
    except in rare cases of significant manufacturing defects, which are evaluated on a case-by-case basis.

    ### 6. Care and Usage
    Jerseys should be washed gently and air-dried to preserve print and fabric quality. 
    The Jersey Forge is not responsible for damage caused by improper care, misuse, or alterations made after purchase.

    ### 7. Acceptance of Terms
    By continuing to the cart and completing your purchase, you acknowledge that you have **read, understood, and agreed** 
    to all of the terms and conditions listed above..
    """)

    if st.button("I Agree — Go to Cart", key="agree_terms"):
        st.session_state.terms_accepted = True
        st.session_state.page = "cart"

    st.button("Back to Store", on_click=go_home, key="back_terms")

# ============================================================
# ======================== CART PAGE =========================
# ============================================================

elif st.session_state.page == "cart":

    st.markdown("<h2 style='color:white;'>Shopping Cart</h2>", unsafe_allow_html=True)

    if not st.session_state.cart:
        st.write("Your cart is empty.")

        if st.button("⬅ Back to Store", key="back_empty_cart"):
            go_home()

        st.stop()

    st.write("---")

    subtotal = 0

    for name, qty in st.session_state.cart.items():

        price = next(p["price"] for p in products if p["name"] == name)
        item_total = price * qty
        subtotal += item_total

        img_col, info_col, price_col = st.columns([1, 4, 1])

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
                "Qty",
                min_value=1,
                max_value=10,
                value=qty,
                key=f"qty_{name}"
            )

            if new_qty != qty:
                st.session_state.cart[name] = new_qty

            if st.button("Delete", key=f"del_{name}"):
                del st.session_state.cart[name]
                st.rerun()

        with price_col:
            st.markdown(f"<h4 style='color:#ffcc66;'>${item_total:.2f}</h4>", unsafe_allow_html=True)

        st.write("---")

    st.markdown(f"<h3 style='color:#ffcc66;'>Subtotal: ${subtotal:.2f}</h3>", unsafe_allow_html=True)

    if st.button("⬅ Back to Store", key="back_cart"):
        go_home()

    st.write("---")

    if st.button("Submit Order", key="submit_order"):
        loading_box = st.empty()
        loading_box.info("Processing your order... Please wait.")
        time.sleep(5)
        loading_box.empty()

        import random
        order_number = random.randint(100000, 999999)

        send_order_email(order_number, st.session_state.cart.copy())

        st.success(f"Order submitted! Your order number is {order_number}, Contact the email mail2divij@gmail.com to get further instructions.")

        st.session_state.cart = {}

# ============================================================
# ======================== WHY US PAGE ========================
# ============================================================

elif st.session_state.page == "whyus":

    st.markdown("<h2 style='color:white;'>Why Us</h2>", unsafe_allow_html=True)

    st.write("""
    I built this website because growing up, I always wanted jerseys — but every time I asked my parents, the answer was the same: they were too expensive. That feeling stuck with me. I remember the disappointment and frustration of wanting to rep my favorite players but not being able to afford it. That’s why this business exists today. I wanted to create a place where people don’t have to feel that same pain, where jerseys are affordable, accessible, and made for real fans who deserve better.
    """)

    st.write("""
    Every jersey we make carries that mission. The work ethic behind each one comes from the promise I made to myself years ago — to build something better than what I had access to. We put care into every stitch, every design, and every order because this isn’t just a business; it’s a passion born from experience. Jerseys for cheap shouldn’t make your wallet weep, and here, they never will. This is quality made with purpose, for fans who deserve the best without breaking the bank.
    """)

    if st.button("⬅ Back to Store", key="back_from_whyus"):
        st.session_state.page = "home"
