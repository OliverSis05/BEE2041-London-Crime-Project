# Final Submission Template

## Title
Which Borough-Level Factors Are Most Strongly Associated with Crime per 1,000 Population Across London?

## 1. Introduction
This project investigates which borough-level factors are most strongly associated with crime per 1,000 population across London boroughs from 2019 to 2024. The analysis uses a cleaned and merged borough-month panel dataset that combines crime, population, population density, labour market claimant counts, and deprivation data. The purpose is to identify whether variation in crime rates is more strongly associated with claimant rate, population density, or deprivation.

## 2. Data and Method
The final dataset contains 2,304 borough-month observations covering 32 London boroughs between 2019 and 2024. Crime per 1,000 population and claimant rate per 1,000 population were calculated to allow fair comparison across boroughs with different population sizes. The analysis was carried out in two stages. First, exploratory analysis was used to summarise borough patterns and time trends. Second, borough-level average values were used to compare simple correlations and standardised regression coefficients across the main predictors.

## 3. Descriptive Findings
The descriptive results show clear variation across boroughs. The highest average crime per 1,000 was recorded in **Westminster (28.77)**, while the lowest was recorded in **Harrow (4.93)**. Over time, the highest yearly mean crime per 1,000 occurred in **2024 (8.86)**, whereas the lowest occurred in **2020 (7.38)**.

[Insert Figure 1 here: /Users/oliver/Documents/bee2041-london-crime-project/output/exploration/figures/mean_crime_per_1000_over_time.png]

[Insert Figure 2 here: /Users/oliver/Documents/bee2041-london-crime-project/output/exploration/figures/top10_boroughs_crime_per_1000.png]

## 4. Simple Relationship Findings
The simple correlation analysis suggests that the strongest positive bivariate relationship with crime per 1,000 is **population_density (0.5293)**. The second strongest is **imd_value (0.2510)**. The weakest simple relationship is **claimant_per_1000 (0.1963)**.

[Insert Figure 3 here: /Users/oliver/Documents/bee2041-london-crime-project/output/exploration/figures/density_vs_crime_rate.png]

## 5. Combined Model Findings
When the predictors are compared together using standardised coefficients, the strongest predictor is **population_density (0.5946)**. The second strongest predictor is **claimant_per_1000 (-0.1937)**. The weakest predictor is **imd_value (0.0676)**.

[Insert Figure 4 here: /Users/oliver/Documents/bee2041-london-crime-project/output/analysis/figures/predictor_strengths.png]

## 6. Main Answer to the Research Question
Taken together, the findings suggest that **population_density** is the strongest borough-level factor associated with crime per 1,000 population in London. This means the evidence from this project points most strongly toward **population_density** as the main explanatory variable among those tested. Although the other variables still matter, they appear less important once all predictors are compared side by side.

## 7. Interpretation
A likely interpretation is that boroughs with greater concentration of people and activity tend to generate more opportunities for recorded crime per 1,000 population. Deprivation may still contribute to differences in crime rates, but the results suggest that it is not the dominant factor once the key variables are assessed together. Claimant rate appears weaker in this borough-level comparison.

## 8. Limitations
- The project uses borough-level averages, so it does not capture within-borough variation.
- The results show association rather than proof of causation.
- Other relevant drivers of crime may not be included in the model.
- The findings depend on the quality and comparability of the borough-level data sources used.

## 9. Conclusion
Overall, the project finds that differences in London crime rates are most strongly associated with population density in the final comparison. The evidence therefore supports the conclusion that denser boroughs tend to record higher crime per 1,000 population, while deprivation has a smaller positive role and claimant rate is comparatively weaker. These findings should be interpreted as evidence of association rather than definitive causation.

## 10. Appendix Reference
Use the appendix tables file for supporting evidence and extra summary tables.