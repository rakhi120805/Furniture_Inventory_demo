import streamlit as st
# st.set_page_config(
#     page_title="Furniture Factory Sahayak",
#     page_icon="🪑",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )
# st.set_page_config(page_title="Furniture Factory Sahayak", page_icon="🪑", layout="wide")
# st.markdown("""
#     <style>
#     /* Background */
#     .stApp {
#         background-color: #f9fff6;
#     }

#     /* Main Title */
#     h1 {
#         color: #2e7d32;
#         text-align: center;
#     }

#     h3 {
#         color: #558b2f;
#         text-align: center;
#     }

#     /* Buttons */
#     div.stButton > button {
#         background-color: #4CAF50;
#         color: white;
#         font-size: 18px;
#         font-weight: bold;
#         height: 70px;
#         border-radius: 12px;
#         border: none;
#     }

#     div.stButton > button:hover {
#         background-color: #388e3c;
#         color: white;
#     }

#     /* Info box */
#     .stAlert {
#         border-radius: 10px;
#     }

#     </style>
# """, unsafe_allow_html=True)
# -----------------------------
# Session State Initialization
# -----------------------------
if "materials" not in st.session_state:
    st.session_state.materials = {
        "Lakdi": {"stock": 100, "unit": "pieces", "low": 20},
        "Screw": {"stock": 200, "unit": "packets", "low": 50},
        "Polish": {"stock": 50, "unit": "cans", "low": 10},
        "Glue": {"stock": 30, "unit": "bottles", "low": 5},
    }

if "products" not in st.session_state:
    st.session_state.products = {
        "Chair": {"Lakdi": 2, "Screw": 8, "Polish": 1},
        "Table": {"Lakdi": 5, "Screw": 16, "Polish": 2, "Glue": 1},
        "Bed": {"Lakdi": 8, "Screw": 30, "Polish": 3, "Glue": 2},
    }

if "production_logs" not in st.session_state:
    st.session_state.production_logs = []

if "page" not in st.session_state:
    st.session_state.page = "home"

materials = st.session_state.materials
products = st.session_state.products
production_logs = st.session_state.production_logs


# -----------------------------
# Navigation Helpers
# -----------------------------
def go_home():
    st.session_state.page = "home"

def go_stock():
    st.session_state.page = "stock"

def go_production():
    st.session_state.page = "production"

def go_report():
    st.session_state.page = "report"


# -----------------------------
# Home Screen
# -----------------------------
def show_home():
    st.markdown(
        "<h1 style='text-align: center; color: #1f3b73;'>Furniture Factory Sahayak</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #444;'>Maal aur Furniture Hisaab Demo</h3>",
        unsafe_allow_html=True
    )

    st.info(
        "Is demo me aap maal dekh sakte hain, furniture banane ki entry kar sakte hain, "
        "aur report me dekh sakte hain ki kya bana aur kya samaan kam bacha hai."
    )

    st.markdown("##")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Maal Kitna Hai", use_container_width=True):
            go_stock()

    with col2:
        if st.button("Naya Furniture Banao", use_container_width=True):
            go_production()

    with col3:
        if st.button("Report Dekho", use_container_width=True):
            go_report()

    st.markdown("##")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Material Types", len(materials))
    with c2:
        st.metric("Total Products", len(products))
    with c3:
        low_count = sum(1 for item in materials.values() if item["stock"] <= item["low"])
        st.metric("Kam Stock Items", low_count)


# -----------------------------
# Stock Screen
# -----------------------------
def show_stock():
    top1, top2 = st.columns([6, 1])
    with top1:
        st.title("Maal Kitna Hai")
    with top2:
        st.button("Home", on_click=go_home, use_container_width=True)

    cols = st.columns(2)
    i = 0
    for material, details in materials.items():
        with cols[i % 2]:
            if details["stock"] <= details["low"]:
                st.error(f"**{material}**\n\n{details['stock']} {details['unit']}  \nKam Stock")
            else:
                st.success(f"**{material}**\n\n{details['stock']} {details['unit']}")
        i += 1


# -----------------------------
# Production Screen
# -----------------------------
def show_production():
    top1, top2 = st.columns([6, 1])
    with top1:
        st.title("Naya Furniture Banao")
    with top2:
        st.button("Home", on_click=go_home, use_container_width=True)

    product_name = st.selectbox("Kaunsa Product?", list(products.keys()))
    quantity = st.number_input("Kitni Quantity?", min_value=1, step=1)

    st.markdown("### Is product me ye samaan lagega:")
    bom = products[product_name]
    for mat, qty in bom.items():
        st.write(f"- {mat}: {qty}")

    if st.button("Banao"):
        required_materials = products[product_name]

        for mat, qty_per_unit in required_materials.items():
            required_qty = qty_per_unit * quantity
            if materials[mat]["stock"] < required_qty:
                st.error(
                    f"{mat} ka stock kam hai. Required: {required_qty}, Available: {materials[mat]['stock']}"
                )
                return

        used_summary = {}
        for mat, qty_per_unit in required_materials.items():
            required_qty = qty_per_unit * quantity
            materials[mat]["stock"] -= required_qty
            used_summary[mat] = required_qty

        production_logs.append({
            "product": product_name,
            "quantity": quantity,
            "used_materials": used_summary
        })

        st.success(f"{quantity} {product_name} successfully ban gaya.")

        st.markdown("### Use hua samaan:")
        for mat, qty in used_summary.items():
            st.write(f"- {mat}: {qty} use hua")

        st.markdown("### Updated Stock:")
        for mat, details in materials.items():
            st.write(f"- {mat}: {details['stock']} {details['unit']}")


# -----------------------------
# Report Screen
# -----------------------------
def show_report():
    top1, top2 = st.columns([6, 1])
    with top1:
        st.title("Report Dekho")
    with top2:
        st.button("Home", on_click=go_home, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Aaj Kya Bana")
        if production_logs:
            for i, log in enumerate(production_logs, start=1):
                st.write(f"**{i}. {log['product']} - {log['quantity']} piece**")
                for mat, qty in log["used_materials"].items():
                    st.write(f"- {mat}: {qty}")
                st.markdown("---")
        else:
            st.info("Abhi tak koi production entry nahi hui hai.")

    with col2:
        st.subheader("Kam Bacha Hua Samaan")
        low_items = []
        for material, details in materials.items():
            if details["stock"] <= details["low"]:
                low_items.append(f"{material} - {details['stock']} {details['unit']}")

        if low_items:
            for item in low_items:
                st.error(item)
        else:
            st.success("Abhi sab samaan theek matra me hai.")


# -----------------------------
# Page Router
# -----------------------------
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "stock":
    show_stock()
elif st.session_state.page == "production":
    show_production()
elif st.session_state.page == "report":
    show_report()