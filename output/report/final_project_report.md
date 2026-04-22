# London Borough Crime Project Report

## 1. Research Question
Which borough-level factors are most strongly associated with crime per 1,000 population across London boroughs from 2019 to 2024?

## 2. Aim of the Project
The aim of this project is to build a borough-level monthly panel dataset for London and use it to examine whether crime rates are most strongly associated with claimant rate, population density, or deprivation.

## 3. Data Used
- Crime data by borough, year, month, crime type and crime subtype.
- Population data by borough and year.
- Population density data by borough.
- Labour market claimant count data by borough, year and month.
- Deprivation data by borough using IMD values.

The final merged dataset contains **2,304 rows** covering **32 London boroughs** observed monthly from **2019 to 2024**.

## 4. Method
The raw datasets were cleaned and standardised so borough names matched across sources. The cleaned datasets were merged into one borough-month panel. Crime per 1,000 population and claimant rate per 1,000 population were then calculated. The analysis was carried out in two stages. First, descriptive and exploratory analysis was used to identify broad patterns across boroughs and over time. Second, borough-level average values were used to compare simple correlations and standardised regression coefficients across the key predictors.

## 5. Descriptive Findings
- The borough with the highest average crime per 1,000 was **Westminster (28.77)**.
- The borough with the lowest average crime per 1,000 was **Harrow (4.93)**.
- The highest yearly mean crime per 1,000 occurred in **2024 (8.86)**.
- The lowest yearly mean crime per 1,000 occurred in **2020 (7.38)**.

## 6. Relationship Findings
Simple correlations suggested that crime per 1,000 was positively associated with population density and deprivation, while the relationship with claimant rate was weaker.
The strongest predictor in the standardised regression comparison was **population_density (0.5946)**.
The weakest predictor was **imd_value (0.0676)**.

## 7. Main Answer to the Research Question
The results suggest that **population density** is the strongest borough-level predictor of crime per 1,000 in this dataset. Deprivation remains positively associated with crime, but its contribution is smaller once the predictors are assessed together. Claimant rate is the weakest of the three core predictors in the combined comparison.

## 8. Interpretation
This implies that more densely populated boroughs tend to experience higher recorded crime rates per 1,000 population. One possible reason is that denser boroughs generate more interaction, movement, commercial activity and opportunities for recorded crime. Deprivation also appears relevant, but the evidence here suggests it is not as strong as density once the variables are assessed side by side.

## 9. Limitations
- This is a borough-level analysis, so it cannot capture variation within boroughs.
- The analysis identifies association, not causation.
- Some potentially important drivers of crime are not included, such as policing intensity, transport flows, income levels or age structure.
- The model explains part of the variation in crime rates, but not all of it.

## 10. Suggested Final Conclusion
Overall, the project finds that variation in crime rates across London boroughs between 2019 and 2024 is most strongly associated with population density. Deprivation has a smaller positive association with crime, while claimant rate is comparatively weak once the predictors are assessed together. This means the evidence from this borough-level panel points most strongly toward density as the main explanatory factor among the variables tested, although the findings should be interpreted as associations rather than definitive causal effects.

## 11. Key Outputs Already Created
- Clean datasets
- Final merged borough-month panel
- Exploration tables and figures
- Analysis tables and predictor comparison
- Final results summary