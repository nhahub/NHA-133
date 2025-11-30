# 🇪🇬 Egyptian Used Cars Full Project: Data Collection to Price Prediction

## 🚀 Project Overview

The Egyptian car market saw a drastic change following the 2022 decision to restrict car imports. This led to a shortage of new cars, pushing most buyers into the used car market. As a result, prices became highly volatile and the market became chaotic.

**The Goal:**
To build a complete system that collects real market data, analyzes it, and creates a Machine Learning (ML) model to help users accurately price their cars based on real market data.

**The Value:**
This project provides a clear, data-driven understanding of the Egyptian used car market, solving the problem of unclear pricing.

## ⚙️ Workflow and Detailed Phases

The project was executed in four main steps:

### Phase 1: Web Scraping
We collected data from the two most important used car websites in Egypt: **Hatla2ee** and **ContactCars**.
* Over **8,000 rows** were scraped from Hatla2ee.
* Over **3,000 rows** were scraped from ContactCars.

### Phase 2: Data Cleaning
The focus was on unifying the format to merge the two datasets. Key steps included:
* **Removing Duplicates:** Deleting repeated ads for accuracy.
* **Standardizing Prices:** Converting text formats (e.g., "1.5 Million") into numeric values.
* **Handling Outliers:** Removing unrealistic values in prices or kilometers.

### Phase 3: EDA & Visualization
We extracted insights and visualized market trends using **Tableau**. The dashboards highlight:
* Best-selling cars in Egypt.
* Price distribution across different Governorates.
* Depreciation rates (drop in price over time).

### Phase 4: Machine Learning Model
An ML model was built to predict car prices based on features like Make, Model, Transmission, and Kilometers.
* **Preprocessing:** Applied feature scaling, encoding, and feature engineering, and dropped unnecessary columns.
* **Algorithms Used:** XGBoost and Random Forest Regressor.
* **Evaluation:** The model achieved high accuracy, evaluated using R2 Score, MAE, and RMSE.

## 📈 Results and Market Insights

Analysis of the market post-2022 revealed significant facts:

| Insight | Detail |
| :--- | :--- |
| **Market Share** | Mercedes-Benz holds approximately **10%** of the used car market. |
| **Price Inflation** | Used car prices are now nearly equal to "Zero" (New) car prices due to import shortages and high demand. |
| **Electric Vehicles (EVs)** | EVs represent less than **1%** of the market, indicating difficulties in modern EV import. |
| **Sales Drop (2022 vs. 2021)** | BMW sales dropped by over 70%, and Chevrolet sales dropped by about 30%. |

### Economic Impact of the Import Restriction
The import restriction, while affecting the market, had positive economic outcomes:
* **Currency Protection:** Saved the country **$4-5 Billion** annually, securing foreign currency for essential goods.
* **Local Manufacturing:** Forced global companies to rely on local assembly instead of easy imports.
* **Regulation:** Closed customs loopholes (such as the misuse of disability car exemptions) to better control state resources.

## 🛠️ Technologies Used

| Category | Tools & Libraries |
| :--- | :--- |
| **Data Collection/Cleaning** | Python (BeautifulSoup, Selenium, Pandas, NumPy) |
| **Visualization** | Tableau Public |
| **Machine Learning** | Scikit-Learn, XGBoost |

## 👥 Team Members

* Abdelrhman Mohamed Yakout (leader)
* Ziad Moursy Oun
* Ahmed Mohmed Hussien
* Abdelrhman Islam Omar
* Ziad Elgendy
* Ahmed Refaay
* Abdelrhman Islam
* Ahmed Refaay
* Ziad Elgendy
