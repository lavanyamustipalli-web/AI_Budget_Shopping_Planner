import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Budget Shopping Planner",
    page_icon="🛍️",
    layout="wide"
)


# ---------------- TITLE ----------------
st.title("🛍️ AI-Based Budget Shopping Planner")
st.write("Plan your shopping smartly and stay within your budget.")


# ---------------- SIDEBAR ----------------
st.sidebar.header("💰 Budget")

budget = st.sidebar.number_input(
    "Enter your total budget (₹)",
    min_value=100,
    value=5000,
    step=100
)


# ---------------- ADD ITEMS ----------------
st.header("🛒 Add Shopping Items")

if "shopping_items" not in st.session_state:
    st.session_state.shopping_items = []


col1, col2, col3, col4 = st.columns(4)

with col1:
    item_name = st.text_input("Item Name")

with col2:
    category = st.selectbox(
        "Category",
        [
            "Clothing",
            "Footwear",
            "Electronics",
            "Grocery",
            "Personal Care",
            "Accessories",
            "Other"
        ]
    )

with col3:
    price = st.number_input(
        "Price (₹)",
        min_value=1,
        value=500
    )

with col4:
    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )


if st.button("➕ Add Item"):
    if item_name.strip():
        st.session_state.shopping_items.append({
            "Item": item_name,
            "Category": category,
            "Price": price,
            "Priority": priority
        })

        st.success(f"{item_name} added successfully!")
    else:
        st.warning("Please enter an item name.")


# ---------------- SHOPPING LIST ----------------
st.header("📋 Shopping List")

if st.session_state.shopping_items:

    df = pd.DataFrame(st.session_state.shopping_items)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    total = df["Price"].sum()
    remaining = budget - total

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Budget", f"₹{budget:,.0f}")

    with col2:
        st.metric("🛒 Total Cost", f"₹{total:,.0f}")

    with col3:
        st.metric(
            "💵 Remaining",
            f"₹{remaining:,.0f}"
        )


    # ---------------- BUDGET STATUS ----------------
    if total <= budget:
        st.success("✅ Your shopping is within budget!")
    else:
        st.error(
            f"⚠️ You exceeded your budget by ₹{total - budget:,.0f}"
        )


    # ---------------- SMART RECOMMENDATION ----------------
    st.header("🤖 Smart Shopping Recommendation")

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    recommendation_df = df.copy()

    recommendation_df["PriorityValue"] = (
        recommendation_df["Priority"].map(priority_order)
    )

    recommendation_df = recommendation_df.sort_values(
        by=["PriorityValue", "Price"]
    )

    selected_items = []
    spent = 0

    for _, row in recommendation_df.iterrows():

        if spent + row["Price"] <= budget:
            selected_items.append(row["Item"])
            spent += row["Price"]

    skipped_items = [
        item for item in df["Item"]
        if item not in selected_items
    ]


    st.subheader("✅ Recommended Items")

    if selected_items:
        for item in selected_items:
            st.write(f"✅ {item}")
    else:
        st.write("No items can currently fit within the budget.")


    if skipped_items:
        st.subheader("❌ Consider Skipping")

        for item in skipped_items:
            st.write(f"❌ {item}")


    # ---------------- CHART ----------------
    st.header("📊 Spending Analysis")

    category_data = df.groupby(
        "Category"
    )["Price"].sum()

    fig, ax = plt.subplots()

    category_data.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Category-wise Shopping Expenses")

    st.pyplot(fig)


else:
    st.info(
        "👆 Add some shopping items to see your budget analysis."
    )


# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "AI-Based Budget Shopping Planner | Python + Streamlit"
)