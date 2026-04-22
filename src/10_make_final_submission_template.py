from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

REPORT_DIR = ROOT / "output" / "report"
EXPL_TABLES = ROOT / "output" / "exploration" / "tables"
EXPL_FIGS = ROOT / "output" / "exploration" / "figures"
ANAL_TABLES = ROOT / "output" / "analysis" / "tables"
ANAL_FIGS = ROOT / "output" / "analysis" / "figures"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

required_files = {
    "borough_summary": EXPL_TABLES / "borough_summary.csv",
    "top10": EXPL_TABLES / "top10_boroughs_by_crime_per_1000.csv",
    "bottom10": EXPL_TABLES / "bottom10_boroughs_by_crime_per_1000.csv",
    "yearly_summary": EXPL_TABLES / "yearly_summary.csv",
    "simple_correlations": ANAL_TABLES / "simple_correlations.csv",
    "ranked_effects": ANAL_TABLES / "ranked_predictor_effects.csv",
}

for name, path in required_files.items():
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {name} -> {path}")

borough_summary = pd.read_csv(required_files["borough_summary"])
top10 = pd.read_csv(required_files["top10"])
bottom10 = pd.read_csv(required_files["bottom10"])
yearly_summary = pd.read_csv(required_files["yearly_summary"])
simple_corr = pd.read_csv(required_files["simple_correlations"])
ranked_effects = pd.read_csv(required_files["ranked_effects"])

borough_summary = borough_summary.sort_values("avg_crime_per_1000", ascending=False).reset_index(drop=True)
yearly_summary = yearly_summary.sort_values("year").reset_index(drop=True)
simple_corr = simple_corr.sort_values("correlation_with_crime_per_1000", ascending=False).reset_index(drop=True)
ranked_effects = ranked_effects.sort_values("abs_effect", ascending=False).reset_index(drop=True)

highest_borough = borough_summary.iloc[0]
lowest_borough = borough_summary.iloc[-1]

highest_year = yearly_summary.loc[yearly_summary["mean_crime_per_1000"].idxmax()]
lowest_year = yearly_summary.loc[yearly_summary["mean_crime_per_1000"].idxmin()]

strongest_simple = simple_corr.iloc[0]
second_simple = simple_corr.iloc[1]
weakest_simple = simple_corr.iloc[-1]

strongest_model = ranked_effects.iloc[0]
second_model = ranked_effects.iloc[1]
weakest_model = ranked_effects.iloc[-1]

template_lines = [
    "# Final Submission Template",
    "",
    "## Title",
    "Which Borough-Level Factors Are Most Strongly Associated with Crime per 1,000 Population Across London?",
    "",
    "## 1. Introduction",
    "This project investigates which borough-level factors are most strongly associated with crime per 1,000 population across London boroughs from 2019 to 2024. The analysis uses a cleaned and merged borough-month panel dataset that combines crime, population, population density, labour market claimant counts, and deprivation data. The purpose is to identify whether variation in crime rates is more strongly associated with claimant rate, population density, or deprivation.",
    "",
    "## 2. Data and Method",
    "The final dataset contains 2,304 borough-month observations covering 32 London boroughs between 2019 and 2024. Crime per 1,000 population and claimant rate per 1,000 population were calculated to allow fair comparison across boroughs with different population sizes. The analysis was carried out in two stages. First, exploratory analysis was used to summarise borough patterns and time trends. Second, borough-level average values were used to compare simple correlations and standardised regression coefficients across the main predictors.",
    "",
    "## 3. Descriptive Findings",
    f"The descriptive results show clear variation across boroughs. The highest average crime per 1,000 was recorded in **{highest_borough['borough']} ({highest_borough['avg_crime_per_1000']:.2f})**, while the lowest was recorded in **{lowest_borough['borough']} ({lowest_borough['avg_crime_per_1000']:.2f})**. Over time, the highest yearly mean crime per 1,000 occurred in **{int(highest_year['year'])} ({highest_year['mean_crime_per_1000']:.2f})**, whereas the lowest occurred in **{int(lowest_year['year'])} ({lowest_year['mean_crime_per_1000']:.2f})**.",
    "",
    f"[Insert Figure 1 here: {EXPL_FIGS / 'mean_crime_per_1000_over_time.png'}]",
    "",
    f"[Insert Figure 2 here: {EXPL_FIGS / 'top10_boroughs_crime_per_1000.png'}]",
    "",
    "## 4. Simple Relationship Findings",
    f"The simple correlation analysis suggests that the strongest positive bivariate relationship with crime per 1,000 is **{strongest_simple['predictor']} ({strongest_simple['correlation_with_crime_per_1000']:.4f})**. The second strongest is **{second_simple['predictor']} ({second_simple['correlation_with_crime_per_1000']:.4f})**. The weakest simple relationship is **{weakest_simple['predictor']} ({weakest_simple['correlation_with_crime_per_1000']:.4f})**.",
    "",
    f"[Insert Figure 3 here: {EXPL_FIGS / 'density_vs_crime_rate.png'}]",
    "",
    "## 5. Combined Model Findings",
    f"When the predictors are compared together using standardised coefficients, the strongest predictor is **{strongest_model['term']} ({strongest_model['standardised_coefficient']:.4f})**. The second strongest predictor is **{second_model['term']} ({second_model['standardised_coefficient']:.4f})**. The weakest predictor is **{weakest_model['term']} ({weakest_model['standardised_coefficient']:.4f})**.",
    "",
    f"[Insert Figure 4 here: {ANAL_FIGS / 'predictor_strengths.png'}]",
    "",
    "## 6. Main Answer to the Research Question",
    f"Taken together, the findings suggest that **{strongest_model['term']}** is the strongest borough-level factor associated with crime per 1,000 population in London. This means the evidence from this project points most strongly toward **{strongest_model['term']}** as the main explanatory variable among those tested. Although the other variables still matter, they appear less important once all predictors are compared side by side.",
    "",
    "## 7. Interpretation",
    "A likely interpretation is that boroughs with greater concentration of people and activity tend to generate more opportunities for recorded crime per 1,000 population. Deprivation may still contribute to differences in crime rates, but the results suggest that it is not the dominant factor once the key variables are assessed together. Claimant rate appears weaker in this borough-level comparison.",
    "",
    "## 8. Limitations",
    "- The project uses borough-level averages, so it does not capture within-borough variation.",
    "- The results show association rather than proof of causation.",
    "- Other relevant drivers of crime may not be included in the model.",
    "- The findings depend on the quality and comparability of the borough-level data sources used.",
    "",
    "## 9. Conclusion",
    "Overall, the project finds that differences in London crime rates are most strongly associated with population density in the final comparison. The evidence therefore supports the conclusion that denser boroughs tend to record higher crime per 1,000 population, while deprivation has a smaller positive role and claimant rate is comparatively weaker. These findings should be interpreted as evidence of association rather than definitive causation.",
    "",
    "## 10. Appendix Reference",
    "Use the appendix tables file for supporting evidence and extra summary tables.",
]

template_path = REPORT_DIR / "final_submission_template.md"
template_path.write_text("\n".join(template_lines), encoding="utf-8")

figure_guide_lines = [
    "FIGURE GUIDE",
    "",
    "1. mean_crime_per_1000_over_time.png",
    "   Use this in the descriptive time-trend section.",
    "",
    "2. top10_boroughs_crime_per_1000.png",
    "   Use this to show borough differences clearly.",
    "",
    "3. density_vs_crime_rate.png",
    "   Use this in the simple relationship section because density is the strongest simple predictor.",
    "",
    "4. predictor_strengths.png",
    "   Use this in the combined model section because it directly answers which factor was strongest.",
    "",
    "5. total_crime_over_time.png",
    "   Optional extra figure if you want a broader trend chart.",
    "",
    "6. claimant_vs_crime_rate.png",
    "   Optional extra figure if you want to discuss why claimant rate is weaker.",
    "",
    "7. deprivation_vs_crime_rate.png",
    "   Optional extra figure if you want to discuss deprivation separately.",
]

figure_guide_path = REPORT_DIR / "figure_placement_guide.txt"
figure_guide_path.write_text("\n".join(figure_guide_lines), encoding="utf-8")

edit_checklist_lines = [
    "FINAL EDIT CHECKLIST",
    "",
    "1. Replace the title with your preferred final title if needed.",
    "2. Check the wording matches your module brief exactly.",
    "3. Add any required academic references if your module expects them.",
    "4. Add the best 3 or 4 figures into the final submission.",
    "5. Keep the answer focused on the research question.",
    "6. Make sure you clearly explain why population_density is the strongest predictor.",
    "7. Keep the causality warning in the limitations section.",
    "8. Proofread the final markdown file before submission.",
]

edit_checklist_path = REPORT_DIR / "final_edit_checklist.txt"
edit_checklist_path.write_text("\n".join(edit_checklist_lines), encoding="utf-8")

print("\n" + "=" * 80)
print("FINAL TEMPLATE FILES CREATED")
print("=" * 80)
print("Submission template:", template_path)
print("Figure guide:", figure_guide_path)
print("Edit checklist:", edit_checklist_path)

print("\n" + "=" * 80)
print("SUBMISSION TEMPLATE PREVIEW")
print("=" * 80)
print("\n".join(template_lines[:45]))

print("\n" + "=" * 80)
print("FIGURE GUIDE PREVIEW")
print("=" * 80)
print("\n".join(figure_guide_lines))

print("\n" + "=" * 80)
print("EDIT CHECKLIST PREVIEW")
print("=" * 80)
print("\n".join(edit_checklist_lines))

