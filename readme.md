# 🌞 Solar Challenge Week 0 — Final Report

*By Yenenesh Dabot*

---

## Introduction

Week 0 of the Solar Challenge aimed to explore the solar energy potential across **three West African countries**: Benin, Sierra Leone, and Togo. The objective was to complete a full data science workflow—from gathering and cleaning the raw data, through exploratory analysis and cross-country comparison, to building an interactive visualization dashboard.

This report presents the workflow and findings in a **storytelling style**, balancing technical rigor with clear, readable narrative.

---

## Project Goals

* Examine solar irradiance and temperature patterns for each country
* Conduct **country-specific exploratory data analysis (EDA)**
* Perform **cross-country comparisons** to identify trends and differences
* Develop an **interactive dashboard** to visualize insights
* Prepare the data and workflow for potential predictive modeling

---

## Data Overview

The datasets included:

| Country      | Filename               | Records      |
| ------------ | -------------------- | ----------- |
| Benin        | benin_clean.csv       | 100,000+    |
| Sierra Leone | sierra_leone_clean.csv | 100,000+   |
| Togo         | togo_clean.csv        | 100,000+    |

**Metrics analyzed:**

* **GHI (Global Horizontal Irradiance):** Total solar radiation received on a horizontal surface
* **DNI (Direct Normal Irradiance):** Direct beam radiation
* **DHI (Diffuse Horizontal Irradiance):** Scattered solar radiation
* **Temperature:** Ambient temperature readings

---

## Workflow Overview

### 1. Project Setup

* Initialized the **GitHub repository** and Python environment
* Installed required packages via `requirements.txt`
* Configured a **CI/CD workflow** using GitHub Actions
* Structured directories for notebooks, scripts, data, and the Streamlit app

---

### 2. Country-Level Exploratory Data Analysis

#### Benin

* **Data Cleaning:** Imputed missing values using median
* **Outlier Detection:** Applied Z-score method
* **Visualization:** Time series plots for GHI, DNI, DHI, and temperature
* **Insights:** Northern regions show the highest solar potential; seasonal patterns are evident

#### Sierra Leone

* **Statistical Analysis:** Computed mean, median, and standard deviation
* **Visualization:** Boxplots and distribution plots for solar metrics
* **Insights:** Coastal regions have higher diffuse radiation, while inland areas show stronger direct irradiance

#### Togo

* **Time Series Analysis:** Seasonal decomposition and trend visualization
* **Correlation Study:** Strong relationship observed between GHI and temperature
* **Insights:** Southern regions experience stable solar exposure, while northern areas show higher variability

---

### 3. Cross-Country Comparison

* **Comparative Metrics:** Analyzed mean, median, and variance across the three countries
* **Regional Patterns:** Northern Benin and Togo show similar GHI trends; Sierra Leone demonstrates coastal-inland differences
* **Benchmarking:** Highlighted top-performing regions for potential solar energy deployment

---


### 4. Interactive Dashboard

* Developed using **Streamlit**
* Key Features:

  * Filter data by country and metric
  * Interactive boxplots and time series charts
  * Export charts for reporting purposes

* Run the dashboard locally:
```bash
streamlit run app/main.py
```
### Key Deliverables
| Component                | Status | Description                         |
| ------------------------ | ------ | ----------------------------------- |
| Benin EDA                | ✅      | Completed                           |
| Sierra Leone EDA         | ✅      | Completed                           |
| Togo EDA                 | ✅      | Completed                           |
| Cross-Country Comparison | ✅      | Completed                           |
| Streamlit Dashboard      | ⏳      | Interactive visualizations deployed |

###  Key Takeaways
Data quality is essential: Proper cleaning and validation improved analysis accuracy

Visualization clarifies patterns: Trends and anomalies became immediately visible

Automation improves reproducibility: Structured workflow and CI/CD pipelines enhanced consistency

Collaboration benefits: Git branching strategies allowed parallel work without conflicts

### Conclusion
Week 0 laid the groundwork for the Solar Challenge by providing cleaned datasets, actionable insights on solar energy potential, and a functional interactive dashboard. This work establishes a solid foundation for future predictive modeling and optimization tasks.

### Tools & References
Python 3.12, Pandas, NumPy, Matplotlib, Seaborn

Streamlit for interactive dashboards

GitHub Actions for CI/CD workflow

Made with  by Yenenesh Dabot