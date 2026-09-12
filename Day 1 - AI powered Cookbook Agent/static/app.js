// ─────────────────────────────────────────────────────────────────────
// INGREDIENT CATEGORIES  (extend freely)
// ─────────────────────────────────────────────────────────────────────
const CATEGORIES = [
  {
    id: "protein",
    icon: "🥩",
    title: "Protein",
    desc: "Pick the proteins you have at home",
    items: [
      { emoji: "🍗", label: "Chicken breast" },
      { emoji: "🥩", label: "Beef" },
      { emoji: "🐖", label: "Pork" },
      { emoji: "🐟", label: "Salmon" },
      { emoji: "🦐", label: "Shrimp" },
      { emoji: "🐟", label: "Tuna" },
      { emoji: "🍖", label: "Turkey" },
      { emoji: "🥓", label: "Bacon" },
      { emoji: "🫘", label: "Chickpeas" },
      { emoji: "🫘", label: "Lentils" },
      { emoji: "🧆", label: "Tofu" },
      { emoji: "🌱", label: "Tempeh" },
    ],
  },
  {
    id: "grains",
    icon: "🌾",
    title: "Grains & Starches",
    desc: "Bases, breads, and carbs",
    items: [
      { emoji: "🍚", label: "Rice" },
      { emoji: "🍝", label: "Pasta" },
      { emoji: "🍞", label: "Bread" },
      { emoji: "🌮", label: "Tortillas" },
      { emoji: "🥔", label: "Potatoes" },
      { emoji: "🍠", label: "Sweet potato" },
      { emoji: "🌽", label: "Corn" },
      { emoji: "🥣", label: "Oats" },
      { emoji: "🫓", label: "Quinoa" },
      { emoji: "🍜", label: "Noodles" },
    ],
  },
  {
    id: "veggies",
    icon: "🥦",
    title: "Vegetables",
    desc: "Fresh, frozen, or canned — all count",
    items: [
      { emoji: "🥦", label: "Broccoli" },
      { emoji: "🧅", label: "Onions" },
      { emoji: "🧄", label: "Garlic" },
      { emoji: "🫑", label: "Bell pepper" },
      { emoji: "🍅", label: "Tomatoes" },
      { emoji: "🥕", label: "Carrots" },
      { emoji: "🥬", label: "Spinach" },
      { emoji: "🥬", label: "Kale" },
      { emoji: "🥒", label: "Cucumber" },
      { emoji: "🌽", label: "Zucchini" },
      { emoji: "🍄", label: "Mushrooms" },
      { emoji: "🌿", label: "Celery" },
      { emoji: "🥑", label: "Avocado" },
      { emoji: "🫛", label: "Peas" },
      { emoji: "🫘", label: "Green beans" },
    ],
  },
  {
    id: "dairy",
    icon: "🧀",
    title: "Dairy",
    desc: "Milk, cheese, cream, and more",
    items: [
      { emoji: "🥛", label: "Milk" },
      { emoji: "🧀", label: "Parmesan" },
      { emoji: "🧀", label: "Cheddar" },
      { emoji: "🧀", label: "Mozzarella" },
      { emoji: "🫙", label: "Greek yogurt" },
      { emoji: "🍶", label: "Heavy cream" },
      { emoji: "🧈", label: "Butter" },
      { emoji: "🫙", label: "Cream cheese" },
      { emoji: "🥛", label: "Oat milk" },
    ],
  },
  {
    id: "eggs",
    icon: "🥚",
    title: "Eggs",
    desc: "The versatile MVP",
    items: [
      { emoji: "🥚", label: "Eggs" },
    ],
  },
  {
    id: "pantry",
    icon: "🧂",
    title: "Pantry & Sauces",
    desc: "Oils, spices, condiments",
    items: [
      { emoji: "🫒", label: "Olive oil" },
      { emoji: "🛢️", label: "Cooking oil" },
      { emoji: "🫙", label: "Soy sauce" },
      { emoji: "🧂", label: "Salt & pepper" },
      { emoji: "🌶️", label: "Chili flakes" },
      { emoji: "🍋", label: "Lemon" },
      { emoji: "🥫", label: "Tomato paste" },
      { emoji: "🥫", label: "Canned tomatoes" },
      { emoji: "🥫", label: "Coconut milk" },
      { emoji: "🫙", label: "Hot sauce" },
      { emoji: "🫙", label: "Mustard" },
      { emoji: "🍯", label: "Honey" },
    ],
  },
  {
    id: "restrictions",
    icon: "🚫",
    title: "Dietary Restrictions",
    desc: "We will filter recipes to match",
    items: [
      { emoji: "🌿", label: "Vegetarian" },
      { emoji: "🌱", label: "Vegan" },
      { emoji: "🥛", label: "No dairy" },
      { emoji: "🌾", label: "Gluten free" },
      { emoji: "🥜", label: "Nut free" },
      { emoji: "🐟", label: "No seafood" },
    ],
  },
  {
    id: "preferences",
    icon: "⚡",
    title: "Meal Preferences",
    desc: "What kind of meals are you after?",
    items: [
      { emoji: "💪", label: "High protein" },
      { emoji: "⚡", label: "Quick meals" },
      { emoji: "🔥", label: "Low calorie" },
      { emoji: "🥩", label: "Meat based" },
      { emoji: "🍱", label: "Batch cooking" },
      { emoji: "🌍", label: "World cuisine" },
      { emoji: "🥗", label: "Light & fresh" },
      { emoji: "🫕", label: "Comfort food" },
    ],
  },
];

// ─────────────────────────────────────────────────────────────────────
// WIZARD STATE
// ─────────────────────────────────────────────────────────────────────
let currentStep = 0;
const selections = {}; // { categoryId: [label, ...] }

// ─────────────────────────────────────────────────────────────────────
// RENDER CURRENT STEP
// ─────────────────────────────────────────────────────────────────────
function renderStep() {
  const cat = CATEGORIES[currentStep];
  const total = CATEGORIES.length;

  // Progress
  document.getElementById("step-label").textContent = `Step ${currentStep + 1} of ${total}`;
  document.getElementById("step-name-label").textContent = cat.title;
  const pct = ((currentStep) / total) * 100;
  document.getElementById("progress-bar").style.width = pct + "%";

  // Header
  document.getElementById("step-icon").textContent = cat.icon;
  document.getElementById("step-title").textContent = cat.title;
  document.getElementById("step-desc").textContent = cat.desc;

  // Back button visibility
  document.getElementById("btn-back").style.visibility = currentStep === 0 ? "hidden" : "visible";

  // Build chip grid
  const grid = document.getElementById("chip-grid");
  grid.innerHTML = "";
  const selected = selections[cat.id] || [];

  cat.items.forEach(({ emoji, label }) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip" + (selected.includes(label) ? " selected" : "");
    btn.innerHTML = `<span class="chip-emoji">${emoji}</span><span>${label}</span>`;
    btn.addEventListener("click", () => {
      btn.classList.toggle("selected");
      updateCountBadge(cat.id);
    });
    grid.appendChild(btn);
  });

  updateCountBadge(cat.id);

  // Show/hide step card vs review
  document.getElementById("step-card").classList.remove("hidden");
  document.getElementById("review-card").classList.add("hidden");
  document.getElementById("result-card").classList.add("hidden");
}

function updateCountBadge(catId) {
  const count = document.querySelectorAll("#chip-grid .chip.selected").length;
  const badge = document.getElementById("count-badge");
  if (count === 0) {
    badge.classList.add("hidden");
  } else {
    badge.classList.remove("hidden");
    badge.textContent = `${count} selected`;
  }
  // Persist in state
  const labels = Array.from(document.querySelectorAll("#chip-grid .chip.selected")).map(
    (c) => c.querySelector("span:last-child").textContent
  );
  selections[catId] = labels;
}

function saveCurrentStep() {
  const cat = CATEGORIES[currentStep];
  const labels = Array.from(document.querySelectorAll("#chip-grid .chip.selected")).map(
    (c) => c.querySelector("span:last-child").textContent
  );
  selections[cat.id] = labels;
}

function goNext() {
  saveCurrentStep();
  if (currentStep < CATEGORIES.length - 1) {
    currentStep++;
    renderStep();
  } else {
    showReview();
  }
}

function goBack() {
  saveCurrentStep();
  if (currentStep > 0) {
    currentStep--;
    renderStep();
  }
}

function skipStep() {
  saveCurrentStep();
  selections[CATEGORIES[currentStep].id] = [];
  if (currentStep < CATEGORIES.length - 1) {
    currentStep++;
    renderStep();
  } else {
    showReview();
  }
}

function backToWizard() {
  document.getElementById("review-card").classList.add("hidden");
  document.getElementById("step-card").classList.remove("hidden");
  renderStep();
}

// ─────────────────────────────────────────────────────────────────────
// REVIEW SCREEN
// ─────────────────────────────────────────────────────────────────────
function showReview() {
  // Progress to 100%
  document.getElementById("progress-bar").style.width = "100%";
  document.getElementById("step-label").textContent = "Review";
  document.getElementById("step-name-label").textContent = "";

  document.getElementById("step-card").classList.add("hidden");
  document.getElementById("review-card").classList.remove("hidden");

  const body = document.getElementById("review-body");
  body.innerHTML = "";

  // Show each ingredient category (not restrictions/preferences — those are below)
  const ingredientCats = CATEGORIES.filter(
    (c) => c.id !== "restrictions" && c.id !== "preferences"
  );
  ingredientCats.forEach((cat) => {
    const picked = selections[cat.id] || [];
    const block = document.createElement("div");
    block.className = "review-category";
    block.innerHTML = `
      <div class="review-category-label">${cat.icon} ${cat.title}</div>
      <div class="flex flex-wrap gap-2">
        ${
          picked.length
            ? picked.map((l) => `<span class="chip-sm selected">${l}</span>`).join("")
            : `<span class="review-category-empty">Nothing selected — skipped</span>`
        }
      </div>
    `;
    body.appendChild(block);
  });

  // Servings
  const servEl = document.getElementById("servings-chips");
  servEl.innerHTML = "";
  [1,2,3,4,5,6].forEach((n) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip-sm" + (n === 2 ? " selected" : "");
    b.textContent = n;
    b.addEventListener("click", () => {
      servEl.querySelectorAll(".chip-sm").forEach((c) => c.classList.remove("selected"));
      b.classList.add("selected");
    });
    servEl.appendChild(b);
  });

  // Days
  const daysEl = document.getElementById("days-chips");
  daysEl.innerHTML = "";
  [1, 3, 5, 7].forEach((d) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip-sm" + (d === 5 ? " selected" : "");
    b.textContent = `${d} day${d > 1 ? "s" : ""}`;
    b.addEventListener("click", () => {
      daysEl.querySelectorAll(".chip-sm").forEach((c) => c.classList.remove("selected"));
      b.classList.add("selected");
    });
    daysEl.appendChild(b);
  });

  // Restrictions (pre-populate from wizard)
  const restEl = document.getElementById("restriction-chips");
  restEl.innerHTML = "";
  const pickedRest = selections["restrictions"] || [];
  CATEGORIES.find((c) => c.id === "restrictions").items.forEach(({ label }) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip-sm" + (pickedRest.includes(label) ? " selected" : "");
    b.textContent = label;
    b.addEventListener("click", () => b.classList.toggle("selected"));
    restEl.appendChild(b);
  });

  // Preferences (pre-populate from wizard)
  const prefEl = document.getElementById("preference-chips");
  prefEl.innerHTML = "";
  const pickedPref = selections["preferences"] || [];
  CATEGORIES.find((c) => c.id === "preferences").items.forEach(({ label }) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip-sm" + (pickedPref.includes(label) ? " selected" : "");
    b.textContent = label;
    b.addEventListener("click", () => b.classList.toggle("selected"));
    prefEl.appendChild(b);
  });
}

// ─────────────────────────────────────────────────────────────────────
// GENERATE PLAN
// ─────────────────────────────────────────────────────────────────────
async function generatePlan() {
  // Gather all ingredient category labels into one flat list
  const ingredientCatIds = CATEGORIES
    .filter((c) => c.id !== "restrictions" && c.id !== "preferences")
    .map((c) => c.id);

  const allIngredients = ingredientCatIds
    .flatMap((id) => selections[id] || [])
    .map((name) => ({ name }));

  const servingsVal = document.querySelector("#servings-chips .chip-sm.selected")?.textContent;
  const daysVal     = document.querySelector("#days-chips .chip-sm.selected")?.textContent;
  const restrictions = Array.from(document.querySelectorAll("#restriction-chips .chip-sm.selected")).map((b) => b.textContent);
  const prefs       = Array.from(document.querySelectorAll("#preference-chips .chip-sm.selected")).map((b) => b.textContent);

  const payload = {
    ingredients: allIngredients,
    dietary_restrictions: restrictions,
    servings:       servingsVal ? Number(servingsVal) : null,
    number_of_days: daysVal    ? Number(daysVal.split(" ")[0]) : null,
    meal_preferences: prefs,
  };

  const btn    = document.getElementById("btn-generate");
  const iconEl = document.getElementById("gen-icon");
  const textEl = document.getElementById("gen-text");

  btn.disabled = true;
  iconEl.innerHTML = `<span class="spinner"></span>`;
  textEl.textContent = "Generating…";

  try {
    const res = await fetch("/api/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(body.detail || res.statusText);
    }
    const plan = await res.json();
    displayResult(plan);
  } catch (err) {
    showToast("Error: " + err.message, 7000);
  } finally {
    btn.disabled = false;
    iconEl.innerHTML = "✨";
    textEl.textContent = "Generate My Meal Plan";
  }
}

// ─────────────────────────────────────────────────────────────────────
// DISPLAY RESULTS
// ─────────────────────────────────────────────────────────────────────
function displayResult(plan) {
  document.getElementById("review-card").classList.add("hidden");
  document.getElementById("step-card").classList.add("hidden");

  const summaryBox = document.getElementById("summary-box");
  if (plan.summary) {
    summaryBox.textContent = plan.summary;
    summaryBox.classList.remove("hidden");
  } else {
    summaryBox.classList.add("hidden");
  }

  const grid = document.getElementById("meals-grid");
  grid.innerHTML = "";
  (plan.meals || []).forEach((meal) => {
    const card = document.createElement("div");
    card.className = "meal-card";
    const safe = (meal.recipe_name || "").replace(/"/g, "&quot;");
    card.innerHTML = `
      <div class="meal-day">Day ${meal.day}</div>
      <div class="meal-name">${meal.recipe_name || "—"}</div>
      <div class="meal-meta">🍽 ${meal.servings || "—"} serving${meal.servings !== 1 ? "s" : ""}</div>
      ${meal.reason ? `<div class="meal-reason">${meal.reason}</div>` : ""}
      <button class="view-recipe-btn" data-recipe="${safe}" onclick="showRecipe(this)">📖 View Recipe</button>
    `;
    grid.appendChild(card);
  });

  document.getElementById("result-card").classList.remove("hidden");
  document.getElementById("result-card").scrollIntoView({ behavior: "smooth" });
}

function startOver() {
  currentStep = 0;
  Object.keys(selections).forEach((k) => delete selections[k]);
  document.getElementById("result-card").classList.add("hidden");
  renderStep();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ─────────────────────────────────────────────────────────────────────
// RECIPE MODAL
// ─────────────────────────────────────────────────────────────────────
async function showRecipe(btn) {
  const name = btn.dataset.recipe;
  if (!window.allRecipes) {
    try {
      const res = await fetch("/api/recipes");
      window.allRecipes = await res.json();
    } catch {
      showToast("Could not load recipe details.");
      return;
    }
  }
  const rec = window.allRecipes.find((r) => r.name === name);
  if (!rec) { showToast("Recipe not found."); return; }

  document.getElementById("modal-title").textContent = rec.name;

  // Tags
  const tagsEl = document.getElementById("modal-tags");
  tagsEl.innerHTML = "";
  (rec.tags || []).forEach((tag) => {
    const s = document.createElement("span");
    s.className = "px-2 py-0.5 bg-blue-50 text-blue-700 text-xs font-medium rounded-full border border-blue-100";
    s.textContent = tag;
    tagsEl.appendChild(s);
  });

  // Meta
  const metaEl = document.getElementById("modal-meta");
  const parts = [];
  if (rec.servings)  parts.push(`🍽 ${rec.servings} servings`);
  if (rec.prep_time) parts.push(`⏱ Prep ${rec.prep_time}`);
  if (rec.cook_time) parts.push(`🔥 Cook ${rec.cook_time}`);
  metaEl.innerHTML = parts.map((p) => `<span>${p}</span>`).join("");

  // Ingredients
  const ingEl = document.getElementById("modal-ingredients");
  ingEl.innerHTML = "";
  (rec.ingredients || []).forEach((ing) => {
    const li = document.createElement("li");
    li.className = "ing-row";
    const qty  = ing.quantity != null ? ing.quantity : "";
    const unit = ing.unit || "";
    li.innerHTML = `<span class="ing-dot"></span><span class="ing-name">${ing.name}</span>${
      qty || unit ? `<span class="ing-qty">${[qty, unit].filter(Boolean).join(" ")}</span>` : ""
    }`;
    ingEl.appendChild(li);
  });

  // Instructions
  const instrEl = document.getElementById("modal-instructions");
  instrEl.innerHTML = "";
  (rec.instructions || []).forEach((step, i) => {
    const li = document.createElement("li");
    li.className = "step-row";
    li.innerHTML = `<span class="step-num">${i + 1}</span><span class="step-text">${step}</span>`;
    instrEl.appendChild(li);
  });

  document.getElementById("recipe-modal").classList.remove("hidden");
}

function closeModal() {
  document.getElementById("recipe-modal").classList.add("hidden");
}
function handleBackdropClick(e) {
  if (e.target === e.currentTarget) closeModal();
}

// ─────────────────────────────────────────────────────────────────────
// TOAST
// ─────────────────────────────────────────────────────────────────────
let toastTimer;
function showToast(msg, duration = 4000) {
  const el = document.getElementById("toast");
  document.getElementById("toast-msg").textContent = msg;
  el.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add("hidden"), duration);
}

// ─────────────────────────────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  renderStep();
  document.getElementById("modal-close").addEventListener("click", closeModal);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });
});
