# 🇪🇬 Egyptian Used Cars Full Project: Data Collection to Price Prediction

## 🚀 Project Overview

[cite_start]The Egyptian car market saw a drastic change following the 2022 decision to restrict car imports[cite: 4]. [cite_start]This led to a shortage of new cars, pushing most buyers into the used car market[cite: 5]. [cite_start]As a result, prices became highly volatile and the market became chaotic[cite: 6].

**The Goal:**
[cite_start]To build a complete system that collects real market data, analyzes it, and creates a Machine Learning (ML) model to help users accurately price their cars[cite: 7].

**The Value:**
[cite_start]This project provides a clear, data-driven understanding of the Egyptian used car market, solving the problem of unclear pricing[cite: 9].

## ⚙️ Workflow and Detailed Phases

[cite_start]The project was executed in four main steps[cite: 11]:

### Phase 1: Web Scraping
[cite_start]We collected data from the two most important used car websites in Egypt: **Hatla2ee** and **ContactCars**[cite: 12].
* [cite_start]Over **8,000 rows** were scraped from Hatla2ee[cite: 19].
* [cite_start]Over **3,000 rows** were scraped from ContactCars[cite: 20].

### Phase 2: Data Cleaning
[cite_start]The focus was on unifying the format to merge the two datasets[cite: 22]. Key steps included:
* [cite_start]**Removing Duplicates:** Deleting repeated ads for accuracy[cite: 23].
* [cite_start]**Standardizing Prices:** Converting text formats (e.g., "1.5 Million") into numeric values[cite: 24].
* [cite_start]**Handling Outliers:** Removing unrealistic values in prices or kilometers[cite: 25].

### Phase 3: EDA & Visualization
[cite_start]We extracted insights and visualized market trends using **Tableau**[cite: 14, 26]. The dashboards highlight:
* [cite_start]Best-selling cars in Egypt[cite: 28].
* [cite_start]Price distribution across different Governorates[cite: 29].
* [cite_start]Depreciation rates (drop in price over time)[cite: 29].

### Phase 4: Machine Learning Model
[cite_start]An ML model was built to predict car prices based on features like Make, Model, Transmission, and Kilometers[cite: 31].
* [cite_start]**Preprocessing:** Applied feature scaling, encoding, and feature engineering, and dropped unnecessary columns[cite: 33].
* [cite_start]**Algorithms Used:** XGBoost and Random Forest Regressor[cite: 34].
* [cite_start]**Evaluation:** The model achieved high accuracy, evaluated using R2 Score, MAE, and RMSE[cite: 35].

## 📈 Results and Market Insights

[cite_start]Analysis of the market post-2022 revealed significant facts[cite: 37]:

| Insight | Detail |
| :--- | :--- |
| **Market Share** | [cite_start]Mercedes-Benz holds approximately **10%** of the used car market[cite: 39]. |
| **Price Inflation** | [cite_start]Used car prices are now nearly equal to "Zero" (New) car prices due to import shortages[cite: 41]. |
| **Electric Vehicles (EVs)** | [cite_start]EVs represent less than **1%** of the market, indicating difficulties in modern EV import[cite: 40]. |
| **Sales Drop (2022 vs. 2021)** | [cite_start]BMW sales dropped by over 70% [cite: 43][cite_start], and Chevrolet sales dropped by about 30%[cite: 45]. |

### Economic Impact of the Import Restriction
[cite_start]The import restriction, while affecting the market, had positive economic outcomes[cite: 47]:
* [cite_start]**Currency Protection:** Saved the country **$4-5 Billion** annually, securing foreign currency for essential goods[cite: 49].
* [cite_start]**Local Manufacturing:** Forced global companies to rely on local assembly instead of easy imports[cite: 50].
* [cite_start]**Regulation:** Closed customs loopholes, such as the misuse of disability car exemptions, to better control state resources[cite: 52].

## 🛠️ Technologies Used

| Category | Tools & Libraries |
| :--- | :--- |
| **Data Collection/Cleaning** | [cite_start]Python (BeautifulSoup, Selenium, Pandas, NumPy) [cite: 54] |
| **Visualization** | [cite_start]Tableau Public [cite: 56] |
| **Machine Learning** | [cite_start]Scikit-Learn, XGBoost [cite: 57] |

## 👥 Team Members

* [cite_start]Abdelrhman Mohamed Yakout (leader) [cite: 59]
* [cite_start]Ziad Oun [cite: 60]
* [cite_start]Ahmed Mohmed Hussien [cite: 61]
* [cite_start]Abdelrhman Islam [cite: 62]
* [cite_start]Ahmed Refaay [cite: 63]
* [cite_start]Ziad Elgendy [cite: 64]
The import restriction, while affecting the market, had positive economic outcomes:
* **Currency Protection:** Saved the country **$4-5 Billion** annually, securing foreign currency for essential goods.
* **Local Manufacturing:** Forced global companies to rely on local assembly instead of easy imports
