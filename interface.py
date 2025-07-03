import streamlit as st
import csv
import os
import pandas as pd
import altair as alt
import io
import subprocess

DATA_FILE = 'expenses.csv'
FIELDNAMES = ['date', 'category', 'amount', 'description']
DEFAULT_CATEGORIES = ["Utility", "Food", "Entertainment"]

# Load expenses from CSV with case-insensitive header handling
def load_expenses():
    expenses = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                normalized_row = {k.strip().lower(): v for k, v in row.items()}
                try:
                    normalized_row['amount'] = float(normalized_row.get('amount', 0))
                except ValueError:
                    normalized_row['amount'] = 0.0
                expenses.append(normalized_row)
    return expenses

# Save a new expense entry
def save_expense(expense):
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(expense)

# Plot a pie chart of expenses by category using Altair
def plot_expenses_by_category(expenses):
    if not expenses:
        st.warning("No expenses to plot.")
        return

    df = pd.DataFrame(expenses)
    dark_palette = [
        "#8ecae6", "#219ebc", "#023047", "#ffb703", "#fb8500",
        "#adb5bd", "#6d6875", "#b5838d", "#ff006e", "#8338ec"
    ]
    categories = df["category"].unique().tolist()
    color_scale = alt.Scale(domain=categories, range=dark_palette[:len(categories)])

    chart = (
        alt.Chart(df)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(field="amount", type="quantitative"),
            color=alt.Color(field="category", type="nominal", scale=color_scale),
            tooltip=["category", "amount"]
        )
        .properties(title="Expenses by Category")
    )
    st.altair_chart(chart, use_container_width=True)

# Get AI recommendation using subprocess and llama3.1:8b

def get_ai_recommendation(df):
    df.columns = [col.lower() for col in df.columns]
    category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    total_expenses = df['amount'].sum()
    top_category = category_totals.index[0]
    top_amount = category_totals.iloc[0]
    top_percentage = (top_amount / total_expenses * 100)

    prompt = f"""
You are a smart financial assistant. Analyze the following:

- Total spent: ${total_expenses:.2f}
- Highest spending category: {top_category} (${top_amount:.2f}, {top_percentage:.1f}% of total)
- Breakdown: {dict(category_totals.head(5))}

Instructions:
1. Should I reduce spending in \"{top_category}\"? Why?
2. Give 2-3 money-saving tips for this category.
3. Suggest a realistic monthly savings goal.

Keep it concise and under 200 words.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1:8b"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        if result.returncode == 0:
            return result.stdout.decode("utf-8").strip()
        else:
            return f"❌ Ollama failed to respond:\n{result.stderr.decode('utf-8')}"
    except FileNotFoundError:
        return "❌ Ollama CLI not found. Make sure it's installed and accessible in PATH."
    except subprocess.TimeoutExpired:
        return "⏳ Model is taking too long. Try a lighter one or simplify your prompt."
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"

# --- Streamlit App Starts Here ---

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💸 Personal Expense Tracker")

# Section: Add new expense
with st.expander("➕ Add New Expense"):
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", DEFAULT_CATEGORIES)
        custom_category = st.text_input("Or type a new category (optional)")
        final_category = custom_category.strip() if custom_category.strip() else category
        amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
        description = st.text_input("Description")
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            new_expense = {
                'date': date.strftime("%Y-%m-%d"),
                'category': final_category,
                'amount': amount,
                'description': description
            }
            save_expense(new_expense)
            st.success("✅ Expense added!")

# Section: Load and display expenses
expenses = load_expenses()

if expenses:
    df = pd.DataFrame(expenses)
    df.columns = [col.capitalize() for col in df.columns]

    st.subheader("📋 Expense History")
    st.dataframe(df)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="Download",
        data=output.getvalue(),
        file_name="expenses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.subheader("📊 Spending Breakdown")
    plot_expenses_by_category(expenses)

    st.subheader("🤖 AI Recommendation")
    if st.button("Get Financial Advice"):
        with st.spinner("Running local LLM analysis with LLaMA 3.1:8B..."):
            ai_response = get_ai_recommendation(df)
            st.markdown("### 💡 Recommendation:")
            # Use a dark background and white text for better visibility in dark mode
            st.markdown(
                """
                <div style='background-color:#222831;padding:16px;border-radius:8px;border-left:4px solid #00adb5;'>
                    <pre style='color:#fff;font-size:1rem;white-space:pre-wrap;margin:0'>{}</pre>
                </div>
                """.format(ai_response),
                unsafe_allow_html=True
            )
else:
    st.info("📝 No expenses recorded yet. Add some to get started!")
