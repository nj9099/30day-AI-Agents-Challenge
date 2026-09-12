# 🍽️ AI Meal Planner — Day 1 of the 30-Day AI Agents Challenge

An intelligent meal-planning agent that turns the ingredients sitting in your kitchen into a personalised weekly meal plan. Built with **LangChain**, **ChromaDB**, **FastAPI**, and a custom selection-based web UI.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| **Chipotle-style wizard** | Step through 8 ingredient categories (Protein, Grains, Veg, Dairy, Eggs, Pantry, Restrictions, Preferences) with visual chip cards |
| **AI meal planning** | GPT-4o-mini generates a coherent multi-day plan matched to what you actually have |
| **Vector similarity search** | ChromaDB retrieves the most relevant recipes before the LLM constructs the plan |
| **Recipe detail modal** | Tap *View Recipe* to see full ingredients and step-by-step instructions |
| **Clean white UI** | Responsive, mobile-friendly design built with Tailwind CSS |
| **FastAPI backend** | REST endpoints for options, recipes, and plan generation |

---

## 🗂️ Project Structure

```
Day 1 - AI powered Cookbook Agent/
├── app.py               # FastAPI entry point & API endpoints
├── main.py              # CLI interface (alternative to the web UI)
├── meal_planner.py      # Core planning logic + LLM calls
├── recipe_loader.py     # Parses markdown recipe files into Python models
├── recipe_documents.py  # Builds ChromaDB vector store from recipes
├── llm.py               # LLM initialisation (OpenAI via LangChain)
├── models.py            # Pydantic data models
├── prompts.py           # LLM system prompts
├── recipes/             # Markdown recipe files
│   ├── broccoli_chicken.md
│   ├── chicken_fried_rice.md
│   └── ...
├── static/              # Web UI assets (served by FastAPI)
│   ├── index.html
│   ├── app.js
│   └── style.css
├── .env.example         # Template for environment variables
└── requirements.txt     # Python dependencies (if present)
```

---

## 🚀 Quick Start

### 1. Clone & enter the project

```bash
git clone <repo-url>
cd "Day 1 - AI powered Cookbook Agent"
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

```bash
cp .env.example .env
# Open .env and paste your key:
# OPENAI_API_KEY=sk-...
```

### 5. Start the web server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000** in your browser.

> **First run note:** The ChromaDB vector store (`chroma_db/`) is built automatically on the first request. No manual seeding needed.

---

## 🖥️ Using the Web UI

1. **Walk through the wizard** — select ingredients across 8 categories (skip any you like)
2. **Review your picks** — adjust servings, number of days, restrictions, and preferences
3. **Generate** — the AI builds your personalised meal plan
4. **View Recipe** — click any meal card to see the full recipe in a modal

---

## 🔌 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the web UI |
| `GET` | `/api/options` | Returns available ingredients, restrictions, and preferences |
| `GET` | `/api/recipes` | Returns all parsed recipes as JSON |
| `POST` | `/api/plan` | Generates a meal plan from a `MealPlanRequest` body |

### Example `POST /api/plan` request

```json
{
  "ingredients": [
    { "name": "chicken breast" },
    { "name": "broccoli" },
    { "name": "rice" }
  ],
  "dietary_restrictions": [],
  "servings": 2,
  "number_of_days": 5,
  "meal_preferences": ["high protein"]
}
```

---

## 🧩 Adding New Recipes

Create a new markdown file in the `recipes/` folder following this format:

```markdown
# Recipe Name

## Description
A short description.

## Ingredients
- 1 lb chicken breast
- 2 cups rice
- ...

## Dietary Information
- High protein
- Dairy free

## Preparation Time
10 minutes

## Cooking Time
20 minutes

## Servings
4

## Instructions
1. Step one.
2. Step two.
```

Delete `chroma_db/` so the vector store is rebuilt with the new recipe on the next server start.

---

## 🛠️ Tech Stack

- **[LangChain](https://langchain.com)** — LLM orchestration & structured output
- **[OpenAI GPT-4o-mini](https://platform.openai.com)** — Meal plan generation
- **[ChromaDB](https://www.trychroma.com)** — Local vector store for recipe retrieval
- **[FastAPI](https://fastapi.tiangolo.com)** — Backend API & static file serving
- **[Tailwind CSS](https://tailwindcss.com)** — UI styling (CDN)

---

## 📄 License

MIT — do whatever you like with it.
