# 🍜 NYC Restaurant Full Expense Dashboard & Cost Modeler

An advanced, data-driven web application built with Python and Streamlit. This operational tool transforms basic ingredient entry into a professional financial modeling platform—allowing NYC restaurateurs to map precise item-by-item profit margins against granular local tax laws and complex urban operating overhead constraints.

## 🚀 Live Link
[👉 Click here to view your live interactive dashboard! 👈](https://nyc-restaurant-food-cost-calculator.streamlit.app/)

---

## 📉 Advanced Financial Architecture

Unlike simple food cost tools, this model accounts for true NYC profit compression by auto-calculating and isolating real operating outlays based on the menu price:

* **Raw Ingredient Food Cost**: Computed dynamically via variable portion and wholesale price mappings.
* **Kitchen Staff Labor**: Set at a fixed **30.0%** industry operational baseline.
* **NYC Combined Sales Tax**: Locked at the standard local **8.875%** revenue withholding rate.
* **Rent & Occupancy**: Fixed at a **10.0%** allocation metric to model strict city commercial leases.
* **Utilities**: Fixed at **5.0%** to capture restaurant power, commercial cooking gas, and water expenses.
* **Marketing & Promotions**: Earmarked at **5.0%** for customer acquisition.
* **Insurance & Local Licenses**: Factored at **4.0%** for localized small business compliance policies.
* **Technology & POS Systems**: Calculated at **3.0%** to clear online ordering and credit card processing swipe fees.
* **Repairs & Maintenance**: Modeled at **3.0%** for recurring heavy back-of-house equipment kitchen upkeep.

---

## 📈 Core Application Modules

* **Multi-Dish Architecture**: Pre-populated with default restaurant staples like *Chicken Fried Rice* and *Beef Lo Mein*.
* **Custom Recipe Engine**: Expandable interface enabling operators to dynamically configure, cost out, and save completely new dishes to the dropdown menu array in real time.
* **Dynamic Cost Partitions**: Interactive parameter controls to change ingredient market costs and recipe proportions side by side.
* **Itemized Expense Allocation Table**: An expandable accounting ledger breaking down exact penny allocations across all nine spending fields.
* **Live Material Volume Graphing**: Renders a dynamic bar chart tracking which specific ingredient represents the highest financial risk factor.
* **'What-If' Monthly Profit Slider**: Projects monthly sales volumes and exact net take-home earnings across a 30-day operating window based on daily orders.

---

## 💻 Technical Stack

* **Language**: Python
* **Web Framework**: Streamlit (Reactive UI inputs, state-cached memory structures, dynamic charting tools)

---

## 🛠️ How to Run Locally

To spin up this development environment locally on your own machine, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com
   ```

2. Navigate into the project directory:
   ```bash
   cd nyc-restaurant-calculator
   ```

3. Install the application dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the Streamlit server instance:
   ```bash
   streamlit run app.py
   ```
