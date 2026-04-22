# Final Results Summary

## 1. Dataset Overview
The final merged dataset contains **2,304 rows**, covering **32 London boroughs** observed monthly from **2019 to 2024**.
The mean crime rate across the panel is **8.21 crimes per 1,000 population**.
Across the full panel, crime per 1,000 ranges from **3.56** to **45.13**.

## 2. Borough-Level Findings
- Highest average crime per 1,000: **Westminster (28.77)**
- Lowest average crime per 1,000: **Harrow (4.93)**
- Gap between highest and lowest borough average: **23.83**

## 3. Time Trend Findings
- Highest yearly mean crime per 1,000: **2024 (8.86)**
- Lowest yearly mean crime per 1,000: **2020 (7.38)**
- Crime falls in the earlier part of the period and rises again by 2023–2024.

## 4. Simple Relationships
- Strongest simple correlation: **population_density (0.5293)**
- Second strongest simple correlation: **imd_value (0.2510)**
- Weakest simple correlation: **claimant_per_1000 (0.1963)**

## 5. Combined Model Findings
- Strongest predictor in the standardised model: **population_density (0.5946)**
- Second strongest predictor: **claimant_per_1000 (-0.1937)**
- Weakest predictor: **imd_value (0.0676)**
- Model R-squared: **0.2937**

## 6. Interpretation
Population density appears to be the strongest factor associated with borough-level crime rates.
Deprivation remains positively related to crime, but the effect is smaller once the predictors are considered together.
Claimant rate does not emerge as the dominant predictor in the combined model.

## 7. Report-Ready Conclusion
The analysis suggests that variation in crime rates across London boroughs is most strongly associated with population density. More densely populated boroughs tend to record higher crime per 1,000 population. Deprivation shows a smaller positive relationship with crime, while claimant rate appears comparatively weak once the predictors are assessed together. This indicates that, within this borough-level dataset, density provides the clearest explanation of differences in recorded crime rates, although the model explains only part of the overall variation and should therefore be interpreted as evidence of association rather than proof of causation.

## 8. Limitation
These findings are based on borough-level averages and a simple standardised regression comparison. They show association, not definitive causation.