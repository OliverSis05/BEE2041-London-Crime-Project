# London Borough Crime Project

If you want to reproduce the full workflow from the scripts, follow these steps in order.

#### 1. Clone the repository

Open Terminal and run:

```bash
git clone YOUR-GITHUB-REPO-URL
cd bee2041-london-crime-project
```

If you downloaded the folder manually instead, just open the project folder in VS Code or Jupyter.

#### 2. Create a virtual environment

This keeps the project packages separate from other Python work.

On macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### 3. Install the required packages

Run:

```bash
pip install -r requirements.txt
```

#### 4. Check the main project structure

Before running anything, make sure these are present:

```text
README.md
blog.ipynb
requirements.txt
data/
src/
output/
```

The project is organised like this:

```text
bee2041-london-crime-project/
├── README.md
├── blog.ipynb
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── clean/
│   └── final/
├── src/
├── output/
│   ├── exploration/
│   ├── analysis/
│   ├── final_results/
│   └── report/
```

#### 5. Run the scripts in order

Run the following scripts one by one:

```bash
python src/03_clean_data.py
python src/05_merge_data.py
python src/06_explore_data.py
python src/07_analyse_relationships.py
python src/08_write_results_summary.py
python src/09_build_report_pack.py
python src/10_make_final_submission_template.py
```

What each script does:

- `03_clean_data.py`  
  Cleans and standardises the raw source files

- `05_merge_data.py`  
  Merges the cleaned files into the final borough-month dataset

- `06_explore_data.py`  
  Creates descriptive tables and figures

- `07_analyse_relationships.py`  
  Compares claimant rate, population density, and deprivation using simple correlations and a standardised regression-style comparison

- `08_write_results_summary.py`  
  Writes the final summary files

- `09_build_report_pack.py`  
  Produces report and appendix support files

- `10_make_final_submission_template.py`  
  Produces the final template and checklist files for submission support

#### 6. Check the final merged dataset

After the merge step, the key file should be:

```text
data/final/london_borough_month_panel.csv
```

This final dataset should have:

- 2304 rows
- 11 columns
- 32 boroughs
- monthly observations from 2019 to 2024
- 0 duplicates
- 0 missing values in the final panel

The final columns are:

- `borough`
- `date`
- `year`
- `month`
- `crime_count`
- `population`
- `crime_per_1000`
- `claimant_count`
- `claimant_per_1000`
- `population_density`
- `imd_value`

If your merged file does not match this, stop and check the earlier scripts before continuing.

#### 7. Check the main output files

After all scripts have run, the most important files should exist.

Main exploration figures:

```text
output/exploration/figures/mean_crime_per_1000_over_time.png
output/exploration/figures/top10_boroughs_crime_per_1000.png
output/exploration/figures/density_vs_crime_rate.png
```

Main analysis figure:

```text
output/analysis/figures/predictor_strengths.png
```

Final summary files:

```text
output/final_results/results_summary.md
output/final_results/results_summary.txt
output/final_results/key_findings.csv
```

Report support files:

```text
output/report/final_project_report.md
output/report/appendix_tables.txt
output/report/submission_checklist.txt
```

If these files exist, the main project pipeline has worked correctly.

#### 8. Open the final notebook

Open:

```text
blog.ipynb
```

This is the final blog-style project output.

If the notebook opens and already shows figures and tables, that is fine.

If it opens without visible outputs, run the cells from top to bottom.

---

## What this project does

This project asks:

**Which borough-level factors are most strongly associated with crime per 1,000 population across London boroughs from 2019 to 2024?**

To answer that question, the project builds a borough-month panel dataset for London and compares crime rates with:

- claimant rate
- population density
- deprivation

The final result is that **population density** is the strongest predictor in this dataset.

---

## Data used

This project combines five borough-level data sources:

1. Crime data by borough, year, month, crime type, and crime subtype
2. Population data by borough and year
3. Population density data by borough
4. Labour market claimant count data by borough, year, and month
5. Deprivation data by borough using IMD values

The cleaned data files are stored in `data/clean/`.

The final merged dataset is stored in:

```text
data/final/london_borough_month_panel.csv
```

---

## Method in simple terms

The project was completed in four main stages:

1. **Cleaning and standardisation**  
   The raw files were cleaned so that borough names matched across datasets.

2. **Merge and variable construction**  
   The cleaned files were merged into one borough-month panel. Two key rates were then created:
   - `crime_per_1000`
   - `claimant_per_1000`

3. **Exploratory analysis**  
   The project produced summary statistics, borough rankings, time trends, and comparison charts.

4. **Relationship analysis**  
   The project compared claimant rate, population density, and deprivation using:
   - simple correlations
   - a standardised regression-style comparison

---

## Main finding

The final results suggest that **population density** is the strongest borough-level factor associated with crime per 1,000 population in this dataset.

In the final comparison:

- population density is the strongest simple relationship
- population density is also the strongest predictor in the combined model
- deprivation remains positively related to crime, but is weaker once the predictors are compared together
- claimant rate does not emerge as the dominant explanation# BEE2041-London-Crime-Project
