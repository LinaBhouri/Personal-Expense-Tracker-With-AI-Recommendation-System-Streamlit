# 💸 Personal Expense Tracker with Local AI (LLaMA 3.1:8B)

Track your expenses and get smart financial recommendations — all **offline**, using a powerful **locally-running LLaMA 3.1:8B** language model.

---

## 📦 Features

- 📝 Add and categorize your daily expenses  
- 📊 Visualize your spending with interactive pie charts (Altair)  
- 📥 Export your data as an Excel file  
- 🤖 Get AI-powered money-saving advice via [Ollama](https://ollama.com) + LLaMA 3.1:8B — no internet or API keys required


---

## 🛠️ Tech Stack

| Tool            | Purpose                                |
|-----------------|----------------------------------------|
| Python + Streamlit | Web interface and interaction        |
| Pandas + CSV    | Data management                        |
| Altair          | Visualization (Pie Chart)              |
| Ollama + LLaMA  | Offline AI reasoning & financial tips  |

---

## 🔧 Installation

1. **Clone this repo**
   ```bash
   git clone https://github.com/LinaBhouri/Personal-Expense-Tracker-With-AI-Recommendation-System-Streamlit.git
   cd Personal-Expense-Tracker-With-AI-Recommendation-System-Streamlit
2.**Install dependencies**
   pip install -r requirements.txt
   
3.**Install & Start Ollama**
# Install Ollama if not already
# https://ollama.com

  ollama pull llama3.1:8b
  ollama serve

4.**Run app**
    streamlit run interface.py

🧠 How It Works
The app collects and stores expense data in expenses.csv, then uses local inference through subprocess to call:

ollama run llama3.1:8b

It sends a natural-language prompt to the LLM, asking for:
-Budget cut suggestions
-Category-specific money-saving tips
-A monthly savings goal




