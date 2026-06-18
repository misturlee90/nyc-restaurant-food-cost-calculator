import streamlit as st

# --- 1. SET UP THE MEMORY BANK (Session State) ---
# If this is the first time loading, pre-populate our menu database
if "menu_database" not in st.session_state:
    st.session_state["menu_database"] = {
        "Chicken Fried Rice": {
            "recipe": {"Chicken": 0.25, "Rice": 0.50, "Egg": 1.00, "Soy Sauce": 1.50, "Oil": 1.00, "Scallions": 2.00},
            "price": 19.95
        },
        "Beef Lo Mein": {
            "recipe": {"Beef": 0.30, "Noodles": 0.50, "Egg": 0.00, "Soy Sauce": 2.00, "Oil": 1.50, "Scallions": 1.00},
            "price": 21.95
        }
    }

st.title("🍜 NYC Chinese Restaurant Cost Dashboard")
st.markdown("Select a dish, customize ingredients, or add an entirely new recipe to the menu.")

# --- 2. THE WHOLESALE LEDGER (Sidebar) ---
st.sidebar.header("Box Wholesale Ingredient Costs ($)")
chicken_cost = st.sidebar.number_input("Chicken (per lb)", value=2.50, step=0.10)
beef_cost = st.sidebar.number_input("Beef (per lb)", value=4.50, step=0.10)
rice_cost = st.sidebar.number_input("Rice (per lb)", value=0.60, step=0.05)
noodles_cost = st.sidebar.number_input("Noodles (per lb)", value=1.10, step=0.05)
egg_cost = st.sidebar.number_input("Egg (per unit)", value=0.15, step=0.05)
soy_sauce_cost = st.sidebar.number_input("Soy Sauce (per oz)", value=0.05, step=0.01)
oil_cost = st.sidebar.number_input("Oil (per oz)", value=0.08, step=0.01)
scallions_cost = st.sidebar.number_input("Scallions (per unit)", value=1.20, step=0.10)

ingredient_costs = {
    "Chicken": chicken_cost, "Beef": beef_cost, "Rice": rice_cost,
    "Noodles": noodles_cost, "Egg": egg_cost, "Soy Sauce": soy_sauce_cost,
    "Oil": oil_cost, "Scallions": scallions_cost
}

# --- 3. CREATING A NEW CUSTOM RECIPE INTERFACE ---
with st.expander("➕ Add a Custom New Recipe to the Menu"):
    custom_name = st.text_input("New Dish Name (e.g., General Tso's Chicken)")
    custom_price = st.number_input("Target Takeout Price ($)", value=15.00, step=0.50)
    
    st.markdown("**Enter Ingredient Quantities for this Custom Dish:**")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        c_chicken = st.number_input("Chicken (lb)", min_value=0.0, value=0.0, key="c_chk")
        c_beef = st.number_input("Beef (lb)", min_value=0.0, value=0.0, key="c_bf")
        c_rice = st.number_input("Rice (lb)", min_value=0.0, value=0.0, key="c_rc")
        c_noodles = st.number_input("Noodles (lb)", min_value=0.0, value=0.0, key="c_ndl")
    with c_col2:
        c_egg = st.number_input("Egg (count)", min_value=0.0, value=0.0, key="c_eg")
        c_soy = st.number_input("Soy Sauce (oz)", min_value=0.0, value=0.0, key="c_sy")
        c_oil = st.number_input("Oil (oz)", min_value=0.0, value=0.0, key="c_ol")
        c_scallion = st.number_input("Scallions (count)", min_value=0.0, value=0.0, key="c_scl")

    # Save button logic
    if st.button("Save Dish to Menu Selection"):
        if custom_name.strip() == "":
            st.error("Please enter a name for your custom dish.")
        else:
            # Build the custom recipe object matching our database format
            new_dish_data = {
                "recipe": {
                    "Chicken": c_chicken, "Beef": c_beef, "Rice": c_rice, "Noodles": c_noodles,
                    "Egg": c_egg, "Soy Sauce": c_soy, "Oil": c_oil, "Scallions": c_scallion
                },
                "price": custom_price
            }
            # Append it straight into our browser memory bank!
            st.session_state["menu_database"][custom_name] = new_dish_data
            st.success(f"✅ '{custom_name}' added successfully! You can now select it in the drop-down menu above.")
            st.rerun()

st.write("---")

# --- 4. THE DYNAMIC DROP-DOWN MENU ---
st.subheader("🍽️ Select a Menu Item to Evaluate")
# Pull the keys (names) out of our session state database dynamically
dish_options = list(st.session_state["menu_database"].keys())
selected_dish = st.selectbox("Choose a dish:", dish_options)

# Load the active selected dish parameters out of memory
active_recipe = st.session_state["menu_database"][selected_dish]["recipe"]
active_price = st.session_state["menu_database"][selected_dish]["price"]

# --- 5. ADJUST ACTIVE DISH RECIPE QUANTITIES ---
st.markdown(f"### 🥣 Adjust Recipe Quantities for **{selected_dish}**")
recipe_qty = {}
cols = st.columns(3)

for index, (ingredient, qty) in enumerate(active_recipe.items()):
    current_col = cols[index % 3]
    with current_col:
        recipe_qty[ingredient] = st.number_input(f"{ingredient} Amount", value=float(qty), step=0.10, key=f"active_{ingredient}")

st.write("---")
menu_price = st.number_input("🥡 Takeout Menu Price ($)", value=float(active_price), step=0.50, key="active_price_box")

# --- 6. MATHEMATICAL BACKEND & CHARTS ---
total_plate_cost = 0.0
chart_data = {}

for ingredient, qty in recipe_qty.items():
    item_cost = qty * ingredient_costs[ingredient]
    total_plate_cost += item_cost
    if qty > 0:
        chart_data[ingredient] = item_cost

food_cost_percentage = (total_plate_cost / menu_price) * 100 if menu_price > 0 else 0
gross_profit = menu_price - total_plate_cost

# Display Results
st.subheader("📊 NYC Financial Analysis")
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Total Plate Cost", f"${total_plate_cost:.2f}")
metric_col2.metric("Food Cost %", f"{food_cost_percentage:.1f}%")
metric_col3.metric("Gross Profit/Plate", f"${gross_profit:.2f}")

if food_cost_percentage <= 15.0:
    st.success("🟢 **STATUS: HIGHLY PROFITABLE**")
elif food_cost_percentage <= 30.0:
    st.warning("🟡 **STATUS: HEALTHY MARGIN**")
else:
    st.error("🔴 **STATUS: WARNING - MARGIN TOO LOW**")

st.write("---")
st.subheader("📈 Expense Breakdown per Ingredient")
st.bar_chart(chart_data)

st.write("---")
st.subheader("💰 'What-If' Monthly Revenue Calculator")
daily_orders = st.slider("Average Orders Sold Per Day:", min_value=0, max_value=200, value=50)
monthly_keepable_profit = (daily_orders * 30) * gross_profit
st.metric("Keepable Margin Profit (Monthly)", f"${monthly_keepable_profit:,.2f}", delta=f"${gross_profit:.2f} per box")
