# 🌾 Ration-Mitr
> **Next-Generation Public Distribution Intelligence**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%2BEngine-150458?logo=pandas)](https://pandas.pydata.org/)

## 📖 Overview

**Ration-Mitr** is an intelligent, real-time command center designed for the Department of Food & Public Distribution. It modernizes India's food distribution network by dynamically tracking migrant mobility to ensure equitable, data-driven food security for every citizen under the "One Nation, One Ration Card" initiative.

### ⚠️ The Problem: Static Allocation in a Dynamic Economy
Currently, the Public Distribution System (PDS) allocates food grains based on static, decadal census data. However, India's workforce is highly mobile. When large populations migrate for seasonal employment, it creates severe data latency. This results in:
* **Critical grain deficits** in high-influx urban districts.
* **Surplus inventory and wastage** in low-density rural areas.

### 💡 The Solution: Dynamic Resource Allocation
Instead of relying on outdated census figures, Ration-Mitr uses administrative metadata (Aadhaar updates) to dynamically track population shifts. It predicts grain demand *before* shortages occur, ensuring resources are routed exactly where they are needed.

---

## 🚀 Core Innovation: The "MigraSense" Metric

Ration-Mitr introduces a novel algorithmic proxy for migration intensity. By analyzing specific demographic metadata, the system filters out natural population growth to isolate migration-driven population shifts. 

**The Logic:**
By comparing the ratio of **Adult Address Updates** to **Child Birth Enrolments**, the system generates a dynamic **Migration Score**. This instantly flags unnatural population spikes in specific districts, allowing for proactive supply chain adjustments.

---

## 🏗️ Technical Architecture

To ensure high-speed processing without the overhead of traditional relational databases, the system utilizes a robust **Flat-File & In-Memory Architecture**:

* **🖥️ Frontend (Streamlit):** A secure, glassmorphism-styled dashboard featuring a real-time horizontal news ticker for live updates.
* **⚙️ Data Engine (Pandas):** High-performance, vectorized batch processing of large CSV shards directly in RAM for zero-latency analytics.
* **🧹 Sanitization Pipeline:** * *Custom Regex:* Strips numerical anomalies from administrative data.
  * *RapidFuzz (AI Fuzzy Matching):* Merges semantic duplicates and spelling variations (e.g., "Bangalore" vs. "Bengaluru").
* **📊 Visualization (Plotly Express):** Renders interactive geospatial data distributions, bar charts, and priority alert tables.

---

## 📈 System Output & Impact

Ration-Mitr instantly categorizes districts into actionable tiers: 
🔴 **CRITICAL** | 🟠 **WARNING** | 🟢 **STABLE**

The live dashboard equips administrators with real-time insights, including:
1. Predicted migrant influxes based on address updates.
2. Identification of critical stress zones.
3. Exact projected grain deficits calculated in Metric Tonnes (MT).

**Impact:** By shifting from static to dynamic allocation, Ration-Mitr prevents localized famine, reduces grain spoilage, and fulfills the true promise of food security for India's mobile workforce.

---

## 🛠️ Getting Started (Local Development)

### Prerequisites
* Python 3.8 or higher
* pip (Python package manager)
