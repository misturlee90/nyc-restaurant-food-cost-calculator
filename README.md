# 🍜 NYC Chinese Restaurant Cost Calculator & Profit Dashboard

An interactive, data-driven web application built with Python and Streamlit. This operational tool helps NYC Chinese takeout restaurants protect their financial margins by calculating real-time plate costs, tracking ingredient expense distributions, and projecting monthly profit volumes.

## 🚀 Live Link
[👉 Click here to view the live interactive app! 👈](https://nyc-restaurant-food-cost-calculator.streamlit.app/)

---

## 📈 Core Features

* **Dynamic Recipe Database**: Comes pre-populated with NYC takeout staples like *Chicken Fried Rice* and *Beef Lo Mein*. 
* **Custom Recipe Engine**: Restaurant owners and chefs can dynamically type in and save completely new dishes to the live menu selection dropdown.
* **Granular Cost Adjustments**: Features simple interfaces to independently scale wholesale package pricing against exact raw recipe portion quantities.
* **Visual Expense Breakdown**: Automatically renders a dynamic bar chart showcasing exactly which ingredient is dominating the plate's cost matrix.
* **"What-If" Volume Calculator**: An interactive volume slider projecting gross monthly revenue and net keepable cash margins based on daily takeout orders.
* **NYC Margin Guardrail**: Employs industry-standard logical status checks tailored to New York City’s high commercial overhead, instantly flagging dishes dipping below sustainable profit thresholds.

---

## 💻 Technical Stack

* **Language**: Python
* **Web Framework**: Streamlit (for UI layout, reactive metric modules, and dynamic charts)

---

## 🛠️ How to Run Locally

If you would like to download and test this codebase on your machine, follow these simple steps:

1. Clone this repository:
   ```bash
   git clone https://github.com
   ```

2. Navigate into the project folder:
   ```bash
   cd nyc-restaurant-calculator
   ```

3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the local web server:
   ```bash
   streamlit run app.py
   ```
