import streamlit as st
import pandas as pd  # <-- Added for spreadsheet data creation

# --- 1. SET UP THE MEMORY BANK (Session State) ---
if "expense_menu_db" not in st.session_state:
    st.session_state["expense_menu_db"] = {
        "Chicken Fried Rice": {
            "recipe": {"Chicken": 0.25, "Rice": 0.50, "Egg": 1.00, "Soy Sauce": 1.50, "Oil": 1.00, "Scallions": 2.00},
            "price": 19.95
        },
        "Beef Lo Mein": {
            "recipe": {"Beef": 0.30, "Noodles": 0.50, "Egg": 0.00, "Soy Sauce": 2.00, "Oil": 1.50, "Scallions": 1.00},
            "price": 21.95
        }
    }

if "reset_counter" not in st.session_state:
    st.session_state["reset_counter"] = 0

st.title("🍜 NYC Restaurant Full Expense Dashboard")
st.markdown("Analyze item-by-item profit margins against granular NYC operating and tax allocations.")

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

# --- 🧾 DYNAMIC ACCOUNTING VALUES (Sidebar) ---
st.sidebar.write("---")
st.sidebar.header("🧾 NYC Tax Configurations")
nyc_sales_tax = st.sidebar.number_input("NYC Combined Sales Tax (%)", value=8.875, step=0.005, format="%.3f")

# Granular breakdown constants
LABOR_PCT = 30.0
RENT_PCT = 10.0
UTILITIES_PCT = 5.0
INSURANCE_PCT = 4.0
MARKETING_PCT = 5.0
TECH_PCT = 3.0
MAINTENANCE_PCT = 3.0

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

    if st.button("Save Dish to Menu Selection"):
        if custom_name.strip() == "":
            st.error("Please enter a name for your custom dish.")
        else:
            st.session_state["expense_menu_db"][custom_name] = {
                "recipe": {
                    "Chicken": c_chicken, "Beef": c_beef, "Rice": c_rice, "Noodles": c_noodles,
                    "Egg": c_egg, "Soy Sauce": c_soy, "Oil": c_oil, "Scallions": c_scallion
                },
                "price": custom_price
            }
            st.success(f"✅ '{custom_name}' added successfully!")
            st.rerun()

st.write("---")

# --- 4. THE DYNAMIC DROP-DOWN MENU ---
st.subheader("🍽️ Select a Menu Item to Evaluate")
dish_options = list(st.session_state["expense_menu_db"].keys())
selected_dish = st.selectbox("Choose a dish:", dish_options)

active_recipe = st.session_state["expense_menu_db"][selected_dish]["recipe"]
active_price = st.session_state["expense_menu_db"][selected_dish]["price"]

if st.button("🔄 Reset This Dish to Defaults"):
    st.session_state["reset_counter"] += 1
    st.rerun()

key_modifier = f"_run_{st.session_state['reset_counter']}"

# --- 5. ADJUST ACTIVE DISH RECIPE QUANTITIES ---
st.markdown(f"### 🥣 Adjust Quantities for {selected_dish}")
recipe_qty = {}
cols = st.columns(3)

for index, (ingredient, qty) in enumerate(active_recipe.items()):
    current_col = cols[index % 3]
    with current_col:
        recipe_qty[ingredient] = st.number_input(f"{ingredient} Amount", value=float(qty), step=0.10, key=f"active_{ingredient}{key_modifier}")

st.write("---")
menu_price = st.number_input("🥡 Takeout Menu Price ($)", value=float(active_price), step=0.50, key=f"active_price_box{key_modifier}")

# --- 6. ADVANCED FINANCIAL MATH ENGINE ---
total_food_cost = 0.0
chart_data = {}

for ingredient, qty in recipe_qty.items():
    item_cost = qty * ingredient_costs[ingredient]
    total_food_cost += item_cost
    if qty > 0:
        chart_data[ingredient] = item_cost

tax_cost = menu_price * (nyc_sales_tax / 100.0)
labor_cost = menu_price * (LABOR_PCT / 100.0)
rent_cost = menu_price * (RENT_PCT / 100.0)
utilities_cost = menu_price * (UTILITIES_PCT / 100.0)
insurance_cost = menu_price * (INSURANCE_PCT / 100.0)
marketing_cost = menu_price * (MARKETING_PCT / 100.0)
tech_cost = menu_price * (TECH_PCT / 100.0)
maintenance_cost = menu_price * (MAINTENANCE_PCT / 100.0)

non_food_operating_costs = tax_cost + labor_cost + rent_cost + utilities_cost + insurance_cost + marketing_cost + tech_cost + maintenance_cost
total_true_cost = total_food_cost + non_food_operating_costs

food_cost_percentage = (total_food_cost / menu_price) * 100 if menu_price > 0 else 0
true_net_takehome = menu_price - total_true_cost
net_margin_percentage = (true_net_takehome / menu_price) * 100 if menu_price > 0 else 0

# Display Metrics Dashboard Grid
st.subheader("📊 Grand Cost Matrix & Margins")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("Raw Food Cost", f"${total_food_cost:.2f}", f"{food_cost_percentage:.1f}% of Price")
metric_col2.metric("NYC Sales Tax", f"${tax_cost:.2f}", f"{nyc_sales_tax}% Rate")
metric_col3.metric("Non-Food Overhead", f"${non_food_operating_costs - tax_cost:.2f}", "63.0% Overhead Total")
metric_col4.metric("True Take-Home Net", f"${true_net_takehome:.2f}", f"{net_margin_percentage:.1f}% Margin")

# Detailed accounting data expandable chart table
with st.expander("📄 View Complete Itemized Expense Allocation Table"):
    st.markdown(f"""

    | Expense Category | Percentage | Allocation per Box (${menu_price:.2f}) |
    | :--- | :--- | :--- |
    | **Takeout Menu Price** | **100.0%** | **${menu_price:.2f}** |
    | Raw Ingredient Food Cost | {food_cost_percentage:.1f}% | ${total_food_cost:.2f} |
    | Kitchen Staff Labor | {LABOR_PCT}% | ${labor_cost:.2f} |
    | NYC Sales Tax | {nyc_sales_tax}% | ${tax_cost:.2f} |
    | Rent & Occupancy | {RENT_PCT}% | ${rent_cost:.2f} |
    | Utilities (Power, Gas, Water) | {UTILITIES_PCT}% | ${utilities_cost:.2f} |
    | Marketing & Promotions | {MARKETING_PCT}% | ${marketing_cost:.2f} |
    | Insurance & Local Licenses | {INSURANCE_PCT}% | ${insurance_cost:.2f} |
    | Technology & POS Fees | {TECH_PCT}% | ${tech_cost:.2f} |
    | Repairs & Maintenance | {MAINTENANCE_PCT}% | ${maintenance_cost:.2f} |
    | **Final Net Take-Home Cash** | **{net_margin_percentage:.1f}%** | **${true_net_takehome:.2f}** |
    """)

# --- 📥 EXPORT TO CSV MECHANISM ---
# 1. Arrange the active math variables into a standard spreadsheet layout
raw_spreadsheet_data = {
    "Expense Category": [
        "Takeout Menu Price", "Raw Ingredient Food Cost", "Kitchen Staff Labor", 
        "NYC Sales Tax", "Rent & Occupancy", "Utilities", "Marketing & Promotions", 
        "Insurance & Local Licenses", "Technology & POS Fees", "Repairs & Maintenance", "Final Net Take-Home Cash"
    ],
    "Percentage Share": [
        "100.0%", f"{food_cost_percentage:.1f}%", f"{LABOR_PCT}%", f"{nyc_sales_tax}%", f"{RENT_PCT}%", 
        f"{UTILITIES_PCT}%", f"{MARKETING_PCT}%", f"{INSURANCE_PCT}%", f"{TECH_PCT}%", f"{MAINTENANCE_PCT}%", f"{net_margin_percentage:.1f}%"
    ],
    "Allocation per Box ($)": [
        menu_price, total_food_cost, labor_cost, tax_cost, rent_cost, 
        utilities_cost, marketing_cost, insurance_cost, tech_cost, maintenance_cost, true_net_takehome
    ]
}

# 2. Convert it into a formal data matrix, then compile it into a raw string file layout
df = pd.DataFrame(raw_spreadsheet_data)
csv_string = df.to_csv(index=False).encode('utf-8')

# 3. Create the layout link button on the dashboard interface
st.download_button(
    label="📥 Download Profit Breakdown Worksheet (CSV)",
    data=csv_string,
    file_name=f"{selected_dish.lower().replace(' ', '_')}_financials.csv",
    mime="text/csv"
)

# Financial Health Alerts
if net_margin_percentage >= 15.0:
    st.success(f"🟢 **STATUS: PROFITABLE ENTERPRISE** — Yielding a safe {net_margin_percentage:.1f}% take-home cushion.")
elif net_margin_percentage >= 5.0:
    st.warning(f"🟡 **STATUS: TIGHT MARGINS** — The item is surviving, but margins are narrow.")
else:
    st.error(f"🔴 **STATUS: LOSING MONEY** — The owner is losing cash on every order due to high operational burdens.")

# --- 7. CHARTS & SLIDERS ---
st.write("---")
st.subheader("📈 Total Cost Share per Ingredient")
st.bar_chart(chart_data)

st.write("---")
st.subheader("💰 'What-If' Monthly Revenue Calculator")
daily_orders = st.slider("Average Orders Sold Per Day:", min_value=0, max_value=200, value=50)
monthly_takehome_profit = (daily_orders * 30) * true_net_takehome
