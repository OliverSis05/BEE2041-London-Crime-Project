from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FINAL_RESULTS = PROJECT_ROOT / "output" / "final_results"
EXPLORATION_TABLES = PROJECT_ROOT / "output" / "exploration" / "tables"
ANALYSIS_TABLES = PROJECT_ROOT / "output" / "analysis" / "tables"
REPORT_DIR = PROJECT_ROOT / "output" / "report"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

required_files = {
    "key_findings": FINAL_RESULTS / "key_findings.csv",
    "results_summary_md": FINAL_RESULTS / "results_summary.md",
    "borough_summary": EXPLORATION_TABLES / "borough_summary.csv",
    "yearly_summary": EXPLORATION_TABLES / "yearly_summary.csv",
    "top10": EXPLORATION_TABLES / "top10_boroughs_by_crime_per_1000.csv",
    "bottom10": EXPLORATION_TABLES / "bottom10_boroughs_by_crime_per_1000.csv",
    "simple_corr": ANALYSIS_TABLES / "simple_correlations.csv",
    "ranked_effects": ANALYSIS_TABLES / "ranked_predictor_effects.csv",
    "std_coefs": ANALYSIS_TABLES / "standardised_regression_coefficients.csv",
}

for name, path in required_files.items():
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {name} -> {path}")

key_findings = pd.read_csv(required_files["key_findings"])
borough_summary = pd.read_csv(required_files["borough_summary"])
yearly_summary = pd.read_csv(required_files["yearly_summary"])
top10 = pd.read_csv(required_files["top10"])
bottom10 = pd.read_csv(required_files["bottom10"])
simple_corr = pd.read_csv(required_files["simple_corr"])
ranked_effects = pd.read_csv(required_files["ranked_effects"])
std_coefs = pd.read_csv(required_files["std_coefs"])

results_summary_md = required_files["results_summary_md"].read_text(encoding="utf-8")

borough_summary = borough_summary.sort_values("avg_crime_per_1000", ascending=False).reset_index(drop=True)
yearly_summary = yearly_summary.sort_values("year").reset_index(drop=True)
simple_corr = simple_corr.sort_values("correlation_with_crime_per_1000", ascending=False).reset_index(drop=True)
ranked_effects = ranked_effects.sort_values("abs_effect", ascending=False).reset_index(drop=True)

highest_borough = borough_summary.iloc[0]
lowest_borough = borough_summary.iloc[-1]
highest_year = yearly_summary.loc[yearly_summary["mean_crime_per_1000"].idxmax()]
lowest_year = yearly_summary.loc[yearly_summary["mean_crime_per_1000"].idxmin()]
strongest_predictor = ranked_effects.iloc[0]
weakest_predictor = ranked_effects.iloc[-1]

report_lines = [
    "# London Borough Crime Project Report",
    "",
    "## 1. Research Question",
    "Which borough-level factors are most strongly associated with crime per 1,000 population across London boroughs from 2019 to 2024?",
    "",
    "## 2. Aim of the Project",
    "The aim of this project is to build a borough-level monthly panel dataset for London and use it to examine whether crime rates are most strongly associated with claimant rate, population density, or deprivation.",
    "",
    "## 3. Data Used",
    "- Crime data by borough, year, month, crime type and crime subtype.",
    "- Population data by borough and year.",
    "- Population density data by borough.",
    "- Labour market claimant count data by borough, year and month.",
    "- Deprivation data by borough using IMD values.",
    "",
    "The final merged dataset contains **2,304 rows** covering **32 London boroughs** observed monthly from **2019 to 2024**.",
    "",
    "## 4. Method",
    "The raw datasets were cleaned and standardised so borough names matched across sources. The cleaned datasets were merged into one borough-month panel. Crime per 1,000 population and claimant rate per 1,000 population were then calculated. The analysis was carried out in two stages. First, descriptive and exploratory analysis was used to identify broad patterns across boroughs and over time. Second, borough-level average values were used to compare simple correlations and standardised regression coefficients across the key predictors.",
    "",
    "## 5. Descriptive Findings",
    f"- The borough with the highest average crime per 1,000 was **{highest_borough['borough']} ({highest_borough['avg_crime_per_1000']:.2f})**.",
    f"- The borough with the lowest average crime per 1,000 was **{lowest_borough['borough']} ({lowest_borough['avg_crime_per_1000']:.2f})**.",
    f"- The highest yearly mean crime per 1,000 occurred in **{int(highest_year['year'])} ({highest_year['mean_crime_per_1000']:.2f})**.",
    f"- The lowest yearly mean crime per 1,000 occurred in **{int(lowest_year['year'])} ({lowest_year['mean_crime_per_1000']:.2f})**.",
    "",
    "## 6. Relationship Findings",
    "Simple correlations suggested that crime per 1,000 was positively associated with population density and deprivation, while the relationship with claimant rate was weaker.",
    f"The strongest predictor in the standardised regression comparison was **{strongest_predictor['term']} ({strongest_predictor['standardised_coefficient']:.4f})**.",
    f"The weakest predictor was **{weakest_predictor['term']} ({weakest_predictor['standardised_coefficient']:.4f})**.",
    "",
    "## 7. Main Answer to the Research Question",
    "The results suggest that **population density** is the strongest borough-level predictor of crime per 1,000 in this dataset. Deprivation remains positively associated with crime, but its contribution is smaller once the predictors are assessed together. Claimant rate is the weakest of the three core predictors in the combined comparison.",
    "",
    "## 8. Interpretation",
    "This implies that more densely populated boroughs tend to experience higher recorded crime rates per 1,000 population. One possible reason is that denser boroughs generate more interaction, movement, commercial activity and opportunities for recorded crime. Deprivation also appears relevant, but the evidence here suggests it is not as strong as density once the variables are assessed side by side.",
    "",
    "## 9. Limitations",
    "- This is a borough-level analysis, so it cannot capture variation within boroughs.",
    "- The analysis identifies association, not causation.",
    "- Some potentially important drivers of crime are not included, such as policing intensity, transport flows, income levels or age structure.",
    "- The model explains part of the variation in crime rates, but not all of it.",
    "",
    "## 10. Suggested Final Conclusion",
    "Overall, the project finds that variation in crime rates across London boroughs between 2019 and 2024 is most strongly associated with population density. Deprivation has a smaller positive association with crime, while claimant rate is comparatively weak once the predictors are assessed together. This means the evidence from this borough-level panel points most strongly toward density as the main explanatory factor among the variables tested, although the findings should be interpreted as associations rather than definitive causal effects.",
    "",
    "## 11. Key Outputs Already Created",
    "- Clean datasets",
    "- Final merged borough-month panel",
    "- Exploration tables and figures",
    "- Analysis tables and predictor comparison",
    "- Final results summary",
]

report_path = REPORT_DIR / "final_project_report.md"
report_path.write_text("\n".join(report_lines), encoding="utf-8")

appendix_lines = [
    "=" * 80,
    "APPENDIX TABLES",
    "=" * 80,
    "",
    "TOP 10 BOROUGHS BY AVERAGE CRIME PER 1000",
    top10.to_string(index=False),
    "",
    "=" * 80,
    "BOTTOM 10 BOROUGHS BY AVERAGE CRIME PER 1000",
    bottom10.to_string(index=False),
    "",
    "=" * 80,
    "YEARLY SUMMARY",
    yearly_summary.to_string(index=False),
    "",
    "=" * 80,
    "SIMPLE CORRELATIONS",
    simple_corr.to_string(index=False),
    "",
    "=" * 80,
    "RANKED PREDICTOR EFFECTS",
    ranked_effects.to_string(index=False),
    "",
    "=" * 80,
    "STANDARDISED REGRESSION COEFFICIENTS",
    std_coefs.to_string(index=False),
]

appendix_path = REPORT_DIR / "appendix_tables.txt"
appendix_path.write_text("\n".join(appendix_lines), encoding="utf-8")

checklist_lines = [
    "FINAL SUBMISSION CHECKLIST",
    "",
    "1. State the research question clearly.",
    "2. Explain the datasets used.",
    "3. Explain how the data was cleaned and merged.",
    "4. State how crime_per_1000 and claimant_per_1000 were calculated.",
    "5. Summarise the descriptive patterns across boroughs.",
    "6. Summarise the time trend across years.",
    "7. Report the simple correlations.",
    "8. Report the standardised regression comparison.",
    "9. State clearly which predictor was strongest.",
    "10. Explain what the result means in plain English.",
    "11. Include limitations and caution about causality.",
    "12. End with a direct answer to the research question.",
    "",
    "FILES TO USE IN WRITE-UP",
    "- output/final_results/results_summary.md",
    "- output/final_results/key_findings.csv",
    "- output/report/final_project_report.md",
    "- output/report/appendix_tables.txt",
]

checklist_path = REPORT_DIR / "submission_checklist.txt"
checklist_path.write_text("\n".join(checklist_lines), encoding="utf-8")

print("\n" + "=" * 80)
print("REPORT FILES CREATED")
print("=" * 80)
print("Main report:", report_path)
print("Appendix:", appendix_path)
print("Checklist:", checklist_path)

print("\n" + "=" * 80)
print("MAIN REPORT PREVIEW")
print("=" * 80)
print("\n".join(report_lines[:35]))

print("\n" + "=" * 80)
print("CHECKLIST PREVIEW")
print("=" * 80)
print("\n".join(checklist_lines))

