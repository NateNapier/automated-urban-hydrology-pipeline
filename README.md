# Automated Urban Hydrology & IDF Curve Pipeline

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

## Project Overview
An end-to-end data engineering and hydrological analysis pipeline that generates statistically realistic precipitation data, validates it against physical constraints, and computes industry-standard **Intensity-Duration-Frequency (IDF) curves** for urban drainage design. 

Calibrated specifically for **Vadodara, Gujarat**, addressing the real-world challenge of cloudburst-induced urban flooding in the Vishwamitri river basin.

## Business & Engineering Impact
**Bridging the Gap:** Translates raw, noisy meteorological data into actionable engineering design parameters (Return Periods, Rainfall Depth, Intensity).
**Climate Resilience:** Uses Extreme Value Theory (Gumbel Distribution) to accurately model tail-risk events (50-year and 100-year storms) that traditional averages miss.
**Automation:** Reduces the time to generate an IDF curve from days of manual Excel/statistical software work to seconds via a reproducible Python pipeline.

## Tech Stack
**Data Processing:** `pandas`, `numpy`
**Statistical Modeling:** `scipy.stats` (Gamma & Generalized Pareto for synthetic generation, Gumbel Extreme Value Type I for IDF fitting)
**Visualization:** `plotly` (Interactive HTML dashboards), `matplotlib`
**Workflow:** Git, GitHub, Virtual Environments

## Key Deliverables
1. **Synthetic Data Generator:** Produces 100+ years of daily rainfall data calibrated to Vadodara's semi-arid monsoon profile (~850mm annual mean, capped at 280mm extreme cloudbursts).
2. **Validation Framework:** Automated checks to ensure synthetic data aligns with real-world physical and climatological constraints.
3. **IDF Curve Engine:** Extracts the Annual Maximum Series (AMS), fits a Gumbel distribution, and outputs expected depths/intensities for 2, 5, 10, 25, 50, and 100-year return periods.

### Sample Output: 24-Hour IDF Curve (Vadodara)
`![IDF Curve](outputs/intensity-duration-frequency-idf-curve-v.png)`
> *Example: 100-Year Storm Expected Depth = 247.4 mm | Intensity = 10.31 mm/hr*

## How to Run
1. Clone the repository and navigate to the folder:
   ```bash
   git clone https://github.com/NateNapier/automated-urban-hydrology-pipeline.git
   cd automated-urban-hydrology-pipeline