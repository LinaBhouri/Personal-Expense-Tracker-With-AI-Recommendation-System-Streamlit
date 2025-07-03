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
2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install & Start Ollama**

> Install Ollama if not already: https://ollama.com

```bash
ollama pull llama3.1:8b
ollama serve
```

4. **Run app**
```bash
streamlit run interface.py
```


### 🧠 How It Works

The app collects and stores expense data in `expenses.csv`, then uses local inference through a subprocess to call:

```bash
ollama run llama3.1:8b
```

It sends a natural-language prompt to the LLM, asking for:

- Budget cut suggestions  
- Category-specific money-saving tips  
- A monthly savings goal

### 🛠️ Tech Stack

| Tool                     | Purpose                        |
|--------------------------|--------------------------------|
| Python + Streamlit       | Web interface and forms        |
| Pandas & CSV            | Data handling and aggregation  |
| Altair                  | Visualizations (Pie Charts)    |
| LLaMA 3.1:8B via Ollama | AI financial recommendations   |

### 📁 File Structure

```plaintext
├── interface.py               # Main Streamlit app
├── expenses.csv               # Local CSV storage (generated at runtime)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
```
### 🤖 Example AI Prompt

The app sends a prompt like this to your local model via subprocess:

```plaintext
You are a smart financial assistant.
Total spent: $1234.56
Highest category: Food ($543.21, 45.2%)
Suggest if this should be reduced, provide 2–3 saving tips, and suggest a realistic savings goal — all under 200 words.
```

### 💡 Sample AI Advice

> “Your highest spending is on Food, accounting for nearly half of your total. Consider reducing eating out and planning meals in advance. You could realistically aim to cut this by 15–20%, saving ~$100/month.”

### 📦 Requirements

- Python 3.8+  
- Streamlit  
- Ollama installed and running  
- LLaMA 3.1:8B model pulled locally via  
  `ollama pull llama3.1:8b`





