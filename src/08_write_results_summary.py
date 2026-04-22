from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPLORATION_TABLES = PROJECT_ROOT / "output" / "exploration" / "tables"
ANALYSIS_TABLES = PROJECT_ROOT / "output" / "analysis" / "tables"
FINAL_RESULTS = PROJECT_ROOT / "output" / "final_results"

FINAL_RESULTS.mkdir(parents=True, exist_ok=True)

required_files = {
    "borough_summary": EXPLORATION_TABLES / "borough_summary.csv",
    "yearly_summary": EXPLORATION_TABLES / "yearly_summary.csv",
    "summary_statistics": EXPLORATION_TABLES / "summary_statistics.csv",
    "simple_correlations": ANALYSIS_TABLES / "simple_correlations.csv",
    "ranked_predictor_effects": ANALYSIS_TABLES / "ranked_predictor_effects.csv",
    "standardised_regression_coefficients": ANALYSIS_TABLES / "standardised_regression_coefficients.csv",
    "analysis_summary": ANALYSIS_TABLES / "analysis_summary.txt",
}

for name, path in required_files.items():
    if not path.exists():
        raise FileNotFoundError(f"Missing required file for {name}: {path}")

borough_summary = pd.read_csv(required_files["borough_summary"])
yearly_summary = pd.read_csv(required_files["yearly_summary"])
summary_statistics = pd.read_csv(required_files["summary_statistics"], index_col=0)
simple_correlations = pd.read_csv(required_files["simple_correlations"])
ranked_effects = pd.read_csv(required_files["ranked_predictor_effects"])
standardised_coefs = pd.read_csv(required_files["standardised_regression_coefficients"])

borough_summary = borough_summary.sort_values("avg_crime_per_1000", ascending=False).reset_index(drop=True)
yearly_summary = yearly_summary.sort_values("year").reset_index(drop=True)
simple_correlations["abs_corr"] = simple_correlations["correlation_with_crime_per_1000"].abs()
simple_correlations = simple_correlations.sort_values("abs_corr", ascending=False).reset_index(drop=True)
ranked_effects = ranked_effects.sort_values("abs_effect", ascending=False).reset_index(drop=True)

highest = borough_summary.iloc[0]
lowest = borough_summary.iloc[-1]

highest_year = yearly_summary.loc[yearly_summary["mean_crime_per_1000"].idxmax()]
lowest_year = yearly_summary.loc[yearly_summary["mean_crime_per_1000"].idxmin()]

crime_mean = summary_statistics.loc["crime_per_1000", "mean"]
crime_min = summary_statistics.loc["crime_per_1000", "min"]
crime_max = summary_statistics.loc["crime_per_1000", "max"]

strongest_simple = simple_correlations.iloc[0]
second_simple = simple_correlations.iloc[1]
weakest_simple = simple_correlations.iloc[-1]

strongest_model = ranked_effects.iloc[0]
second_model = ranked_effects.iloc[1]
weakest_model = ranked_effects.iloc[-1]

analysis_summary_text = required_files["analysis_summary"].read_text().strip().splitlines()
r_squared_line = next((line for line in analysis_summary_text if line.lower().startswith("r-squared:")), None)
r_squared_value = r_squared_line.split(":")[1].strip() if r_squared_line else "Not found"

key_findings = pd.DataFrame([
    {"metric": "Highest average crime per 1000 borough", "value": highest["borough"]},
    {"metric": "Highest average crime per 1000 value", "value": round(highest["avg_crime_per_1000"], 4)},
    {"metric": "Lowest average crime per 1000 borough", "value": lowest["borough"]},
    {"metric": "Lowest average crime per 1000 value", "value": round(lowest["avg_crime_per_1000"], 4)},
    {"metric": "Highest yearly mean crime per 1000", "value": f"{int(highest_year['year'])} ({highest_year['mean_crime_per_1000']:.4f})"},
    {"metric": "Lowest yearly mean crime per 1000", "value": f"{int(lowest_year['year'])} ({lowest_year['mean_crime_per_1000']:.4f})"},
    {"metric": "Strongest simple correlation", "value": f"{strongest_simple['predictor']} ({strongest_simple['correlation_with_crime_per_1000']:.4f})"},
    {"metric": "Second strongest simple correlation", "value": f"{second_simple['predictor']} ({second_simple['correlation_with_crime_per_1000']:.4f})"},
    {"metric": "Weakest simple correlation", "value": f"{weakest_simple['predictor']} ({weakest_simple['correlation_with_crime_per_1000']:.4f})"},
    {"metric": "Strongest model predictor", "value": f"{strongest_model['term']} ({strongest_model['standardised_coefficient']:.4f})"},
    {"metric": "Second strongest model predictor", "value": f"{second_model['term']} ({second_model['standardised_coefficient']:.4f})"},
    {"metric": "Weakest model predictor", "value": f"{weakest_model['term']} ({weakest_model['standardised_coefficient']:.4f})"},
    {"metric": "Model R-squared", "value": r_squared_value},
])

key_findings_path = FINAL_RESULTS / "key_findings.csv"
key_findings.to_csv(key_findings_path, index=False)

text_lines = [
    "=" * 80,
    "FINAL RESULTS SUMMARY",
    "=" * 80,
    "",
    "1. DATASET OVERVIEW",
    f"- The final merged dataset contains 2,304 rows, representing 32 London boroughs observed monthly from 2019 to 2024.",
    f"- The mean crime rate across the panel is {crime_mean:.2f} crimes per 1,000 population.",
    f"- Across the full panel, crime per 1,000 ranges from {crime_min:.2f} to {crime_max:.2f}.",
    "",
    "2. BOROUGH-LEVEL FINDINGS",
    f"- The borough with the highest average crime per 1,000 is {highest['borough']} at {highest['avg_crime_per_1000']:.2f}.",
    f"- The borough with the lowest average crime per 1,000 is {lowest['borough']} at {lowest['avg_crime_per_1000']:.2f}.",
    f"- The gap between the highest and lowest borough average is {highest['avg_crime_per_1000'] - lowest['avg_crime_per_1000']:.2f} crimes per 1,000.",
    "",
    "3. TIME TREND FINDINGS",
    f"- The highest yearly mean crime per 1,000 occurs in {int(highest_year['year'])} at {highest_year['mean_crime_per_1000']:.2f}.",
    f"- The lowest yearly mean crime per 1,000 occurs in {int(lowest_year['year'])} at {lowest_year['mean_crime_per_1000']:.2f}.",
    f"- Crime falls in the early part of the period and then rises again by 2023–2024.",
    "",
    "4. SIMPLE RELATIONSHIPS",
    f"- The strongest simple correlation with crime per 1,000 is {strongest_simple['predictor']} ({strongest_simple['correlation_with_crime_per_1000']:.4f}).",
    f"- The second strongest simple correlation is {second_simple['predictor']} ({second_simple['correlation_with_crime_per_1000']:.4f}).",
    f"- The weakest simple correlation is {weakest_simple['predictor']} ({weakest_simple['correlation_with_crime_per_1000']:.4f}).",
    "",
    "5. COMBINED MODEL FINDINGS",
    f"- In the standardised regression comparison, the strongest predictor is {strongest_model['term']} ({strongest_model['standardised_coefficient']:.4f}).",
    f"- The second strongest predictor is {second_model['term']} ({second_model['standardised_coefficient']:.4f}).",
    f"- The weakest predictor is {weakest_model['term']} ({weakest_model['standardised_coefficient']:.4f}).",
    f"- The model R-squared is {r_squared_value}.",
    "",
    "6. INTERPRETATION",
    f"- Population density appears to be the strongest factor associated with differences in crime rates across boroughs.",
    f"- Deprivation remains positively related to crime, but its effect is much smaller once the other predictors are considered together.",
    f"- Claimant rate does not emerge as the dominant predictor in the combined model and becomes weaker once density and deprivation are included.",
    "",
    "7. REPORT-READY CONCLUSION",
    "The analysis suggests that variation in crime rates across London boroughs is most strongly associated with population density.",
    "More densely populated boroughs tend to record higher crime per 1,000 population.",
    "Deprivation shows a smaller positive relationship with crime, while claimant rate appears comparatively weak once the predictors are assessed together.",
    "This means that, within this borough-level dataset, density provides the clearest explanation of differences in recorded crime rates, although the model explains only part of the overall variation and should therefore be interpreted as evidence of association rather than proof of causation.",
    "",
    "8. CAUTION / LIMITATION",
    "These findings are based on borough-level averages and a simple standardised regression comparison.",
    "They identify patterns of association, not definitive causal effects.",
    "",
    "=" * 80,
    "END OF SUMMARY",
    "=" * 80,
]

text_output_path = FINAL_RESULTS / "results_summary.txt"
text_output_path.write_text("\n".join(text_lines), encoding="utf-8")

md_lines = [
    "# Final Results Summary",
    "",
    "## 1. Dataset Overview",
    f"The final merged dataset contains **2,304 rows**, covering **32 London boroughs** observed monthly from **2019 to 2024**.",
    f"The mean crime rate across the panel is **{crime_mean:.2f} crimes per 1,000 population**.",
    f"Across the full panel, crime per 1,000 ranges from **{crime_min:.2f}** to **{crime_max:.2f}**.",
    "",
    "## 2. Borough-Level Findings",
    f"- Highest average crime per 1,000: **{highest['borough']} ({highest['avg_crime_per_1000']:.2f})**",
    f"- Lowest average crime per 1,000: **{lowest['borough']} ({lowest['avg_crime_per_1000']:.2f})**",
    f"- Gap between highest and lowest borough average: **{highest['avg_crime_per_1000'] - lowest['avg_crime_per_1000']:.2f}**",
    "",
    "## 3. Time Trend Findings",
    f"- Highest yearly mean crime per 1,000: **{int(highest_year['year'])} ({highest_year['mean_crime_per_1000']:.2f})**",
    f"- Lowest yearly mean crime per 1,000: **{int(lowest_year['year'])} ({lowest_year['mean_crime_per_1000']:.2f})**",
    "- Crime falls in the earlier part of the period and rises again by 2023–2024.",
    "",
    "## 4. Simple Relationships",
    f"- Strongest simple correlation: **{strongest_simple['predictor']} ({strongest_simple['correlation_with_crime_per_1000']:.4f})**",
    f"- Second strongest simple correlation: **{second_simple['predictor']} ({second_simple['correlation_with_crime_per_1000']:.4f})**",
    f"- Weakest simple correlation: **{weakest_simple['predictor']} ({weakest_simple['correlation_with_crime_per_1000']:.4f})**",
    "",
    "## 5. Combined Model Findings",
    f"- Strongest predictor in the standardised model: **{strongest_model['term']} ({strongest_model['standardised_coefficient']:.4f})**",
    f"- Second strongest predictor: **{second_model['term']} ({second_model['standardised_coefficient']:.4f})**",
    f"- Weakest predictor: **{weakest_model['term']} ({weakest_model['standardised_coefficient']:.4f})**",
    f"- Model R-squared: **{r_squared_value}**",
    "",
    "## 6. Interpretation",
    "Population density appears to be the strongest factor associated with borough-level crime rates.",
    "Deprivation remains positively related to crime, but the effect is smaller once the predictors are considered together.",
    "Claimant rate does not emerge as the dominant predictor in the combined model.",
    "",
    "## 7. Report-Ready Conclusion",
    "The analysis suggests that variation in crime rates across London boroughs is most strongly associated with population density. More densely populated boroughs tend to record higher crime per 1,000 population. Deprivation shows a smaller positive relationship with crime, while claimant rate appears comparatively weak once the predictors are assessed together. This indicates that, within this borough-level dataset, density provides the clearest explanation of differences in recorded crime rates, although the model explains only part of the overall variation and should therefore be interpreted as evidence of association rather than proof of causation.",
    "",
    "## 8. Limitation",
    "These findings are based on borough-level averages and a simple standardised regression comparison. They show association, not definitive causation.",
]

md_output_path = FINAL_RESULTS / "results_summary.md"
md_output_path.write_text("\n".join(md_lines), encoding="utf-8")

print("\n" + "=" * 80)
print("FINAL RESULTS FILES CREATED")
print("=" * 80)
print("Text summary:", text_output_path)
print("Markdown summary:", md_output_path)
print("Key findings table:", key_findings_path)

print("\n" + "=" * 80)
print("KEY FINDINGS")
print("=" * 80)
print(key_findings.to_string(index=False))

print("\n" + "=" * 80)
print("REPORT-READY CONCLUSION")
print("=" * 80)
print(md_lines[-3])