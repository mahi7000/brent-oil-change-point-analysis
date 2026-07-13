# Birhan Energies — Brent Oil Change Point Analysis & Statistical Modeling

This repository contains the complete modular data pipeline, exploratory notebooks, and Bayesian statistical architectures required to analyze and model how major political, geopolitical, and economic shocks alter historical Brent crude oil pricing structures.

## 📄 Section 1: End-to-End Data Analysis Workflow Plan
1. **Data Ingestion & Modular Cleaning:** Load raw transaction files, execute whitespace stripping across column headers, parse mixed-mode date representations dynamically, sort chronologically, and impute weekend/holiday market gaps using multi-directional forward-filling blocks.
2. **Exploratory Data Analysis (EDA):** Isolate broad macroeconomic tendencies using a 365-day moving average. Run formalized stationarity check arrays via the Augmented Dickey-Fuller (ADF) test metric. Transform nominal price tracks into continuous log returns.
3. **Bayesian Change Point Modeling:** Formulate a robust stochastic architecture inside `PyMC`. The framework isolates structural variations by defining a discrete uniform prior over the index timeline ($\tau$) and utilizing exponential distributions to capture behavioral parameters before and after shifts.
4. **MCMC Convergence Diagnostics & Event Attribution:** Approximate joint posterior distributions, verify chain health via Gelman-Rubin convergence parameters ($\hat{R} \approx 1.0$), and cross-reference median break indices against the curated geopolitical event baseline.
5. **Dashboard Deployment:** Expose optimized key-value model data parameters over modular Flask API endpoints to feed an interactive, responsive graphing dashboard interface implemented in React.

## 🧠 Section 2: Modeling Foundations, Assumptions, and Limitations

### Conceptual Mechanics of Change Point Models
A Bayesian Change Point model maps out sudden structural adjustments in the underlying process that generates time series data. Instead of forcing global parameters across decades of volatile market movements, the model isolates structural transitions into clear, independent regimes.

*   **Expected Outputs:**
    *   **The Switch Point Index ($\tau$):** A continuous posterior probability distribution flagging the calendar date of the regime transition.
    *   **Regime Variations ($\sigma_1, \sigma_2$):** Direct statistical estimates quantifying behavioral conditions before and after the change point.

### Crucial Assumptions & Core Analytical Caveats
*   **The Discreteness Assumption:** Standard change point systems operate under the constraint that market regimes switch instantaneously at a single index day ($\tau$). In actual energy markets, adjustments can materialize gradually as speculative positions settle.
*   **Temporal Correlation vs. Causal Impact:**
    > ⚠️ **CRITICAL NOTE:** Discovering a statistical change point that lines up perfectly with a calendar date confirms a **temporal correlation in time**, but it does **not** serve as absolute proof of direct causality. The model flags *when* the data distribution shifted; it requires external qualitative context to link that break to a real-world event. Analysts must remain aware that hidden, unobserved macroeconomic factors could be the true underlying drivers behind these shifts.

## 🛠️ Operational Setup
1. Create a clean virtual environment: `python3 -m venv venv && source venv/bin/activate`
2. Install structured dependencies: `pip install -r requirements.txt`
3. Execute the diagnostic workspace pipeline: `python scripts/run_eda.py`

## 🖥️ Section 3: Interactive Dashboard Deployment Engine

Our dashboard application uses a dual-runtime architecture, pairing a Python Flask REST service with a decoupled React user interface web app.

### 1. Initializing the Flask Backend Service Engine
From your system terminal panel inside your active virtual workspace, run these layout setup calls:
```bash
# Ensure required packages are globally synchronized
pip install flask flask-cors pandas numpy

# Spin up the development API channel server
python app.py